"""
Analytics API Routes
AI-powered analytics and insights
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.price_history import PriceHistory
from app.models.product import Product
from app.models.competitor import Competitor
from app.services.ollama_service import OllamaService
from datetime import datetime, timedelta

router = APIRouter()
ollama_service = OllamaService()

class PricingRecommendation(BaseModel):
    recommended_price: float
    strategy: str
    reasoning: str
    confidence: float

class MarketInsight(BaseModel):
    product_id: int
    product_name: str
    average_price: float
    min_price: float
    max_price: float
    price_trend: str  # "increasing", "decreasing", "stable"
    competitor_count: int

@router.get("/recommendation/{product_id}", response_model=PricingRecommendation)
async def get_pricing_recommendation(product_id: int, db: Session = Depends(get_db)):
    """Get AI-powered pricing recommendation for a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get latest prices from all competitors
    latest_prices = db.query(
        PriceHistory.competitor_id,
        func.max(PriceHistory.timestamp).label('max_timestamp')
    ).filter(
        PriceHistory.product_id == product_id
    ).group_by(PriceHistory.competitor_id).all()
    
    competitor_prices = []
    for comp_id, _ in latest_prices:
        price_record = db.query(PriceHistory).filter(
            PriceHistory.product_id == product_id,
            PriceHistory.competitor_id == comp_id
        ).order_by(desc(PriceHistory.timestamp)).first()
        
        if price_record:
            competitor_prices.append(price_record.price)
    
    current_price = product.base_price or (competitor_prices[0] if competitor_prices else 0)
    
    recommendation = await ollama_service.generate_pricing_recommendation(
        product_name=product.name,
        current_price=current_price,
        competitor_prices=competitor_prices
    )
    
    return recommendation

@router.get("/insights", response_model=List[MarketInsight])
async def get_market_insights(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get market insights for all products"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    products = db.query(Product).all()
    insights = []
    
    for product in products:
        prices = db.query(PriceHistory).filter(
            PriceHistory.product_id == product.id,
            PriceHistory.timestamp >= start_date
        ).all()
        
        if not prices:
            continue
        
        price_list = [p.price for p in prices]
        avg_price = sum(price_list) / len(price_list)
        min_price = min(price_list)
        max_price = max(price_list)
        
        # Determine trend (simple: compare first half vs second half)
        if len(price_list) > 10:
            first_half = price_list[:len(price_list)//2]
            second_half = price_list[len(price_list)//2:]
            first_avg = sum(first_half) / len(first_half)
            second_avg = sum(second_half) / len(second_half)
            
            if second_avg > first_avg * 1.05:
                trend = "increasing"
            elif second_avg < first_avg * 0.95:
                trend = "decreasing"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        # Count unique competitors
        competitor_ids = set([p.competitor_id for p in prices])
        
        insights.append(MarketInsight(
            product_id=product.id,
            product_name=product.name,
            average_price=avg_price,
            min_price=min_price,
            max_price=max_price,
            price_trend=trend,
            competitor_count=len(competitor_ids)
        ))
    
    return insights

@router.get("/competitor-analysis/{competitor_id}")
async def get_competitor_analysis(competitor_id: int, db: Session = Depends(get_db)):
    """Analyze competitor pricing strategy"""
    competitor = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    
    # Get all products tracked for this competitor
    prices = db.query(PriceHistory).filter(
        PriceHistory.competitor_id == competitor_id
    ).order_by(desc(PriceHistory.timestamp)).all()
    
    # Group by product
    product_prices = {}
    for price in prices:
        if price.product_id not in product_prices:
            product_prices[price.product_id] = price.price
    
    if not product_prices:
        return {
            "competitor_id": competitor_id,
            "competitor_name": competitor.name,
            "message": "No price data available"
        }
    
    price_list = list(product_prices.values())
    avg_price = sum(price_list) / len(price_list)
    
    # Count promotions
    promotions = db.query(PriceHistory).filter(
        PriceHistory.competitor_id == competitor_id,
        PriceHistory.promotion_active == 1
    ).count()
    
    return {
        "competitor_id": competitor_id,
        "competitor_name": competitor.name,
        "products_tracked": len(product_prices),
        "average_price": avg_price,
        "active_promotions": promotions,
        "pricing_strategy": "competitive" if promotions > len(product_prices) * 0.3 else "standard"
    }



