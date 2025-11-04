"""
Price History API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.price_history import PriceHistory
from app.models.product import Product
from app.models.competitor import Competitor
from datetime import datetime, timedelta

router = APIRouter()

class PriceHistoryCreate(BaseModel):
    product_id: int
    competitor_id: int
    price: float
    currency: Optional[str] = "USD"
    availability: Optional[int] = 1
    sale_price: Optional[float] = None
    discount_percentage: Optional[float] = None
    promotion_active: Optional[int] = 0

class PriceHistoryResponse(BaseModel):
    id: int
    product_id: int
    competitor_id: int
    price: float
    currency: str
    availability: int
    sale_price: Optional[float]
    discount_percentage: Optional[float]
    promotion_active: int
    timestamp: datetime
    product_name: Optional[str] = None
    competitor_name: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=PriceHistoryResponse)
async def create_price_history(price: PriceHistoryCreate, db: Session = Depends(get_db)):
    """Record a new price"""
    # Verify product and competitor exist
    product = db.query(Product).filter(Product.id == price.product_id).first()
    competitor = db.query(Competitor).filter(Competitor.id == price.competitor_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    
    db_price = PriceHistory(**price.dict())
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    
    # Add product and competitor names
    response = PriceHistoryResponse.from_orm(db_price)
    response.product_name = product.name
    response.competitor_name = competitor.name
    return response

@router.get("/product/{product_id}", response_model=List[PriceHistoryResponse])
async def get_product_price_history(
    product_id: int,
    days: Optional[int] = Query(30, ge=1, le=365),
    competitor_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get price history for a product"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id,
        PriceHistory.timestamp >= start_date
    )
    
    if competitor_id:
        query = query.filter(PriceHistory.competitor_id == competitor_id)
    
    prices = query.order_by(desc(PriceHistory.timestamp)).all()
    
    # Add product and competitor names
    product = db.query(Product).filter(Product.id == product_id).first()
    result = []
    for price in prices:
        competitor = db.query(Competitor).filter(Competitor.id == price.competitor_id).first()
        response = PriceHistoryResponse.from_orm(price)
        response.product_name = product.name if product else None
        response.competitor_name = competitor.name if competitor else None
        result.append(response)
    
    return result

@router.get("/compare", response_model=List[PriceHistoryResponse])
async def compare_prices(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get current prices from all competitors for a product"""
    # Get latest price from each competitor
    latest_prices = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id
    ).order_by(
        desc(PriceHistory.timestamp)
    ).all()
    
    # Group by competitor and get latest
    competitor_latest = {}
    for price in latest_prices:
        if price.competitor_id not in competitor_latest:
            competitor_latest[price.competitor_id] = price
    
    result = []
    product = db.query(Product).filter(Product.id == product_id).first()
    for competitor_id, price in competitor_latest.items():
        competitor = db.query(Competitor).filter(Competitor.id == competitor_id).first()
        response = PriceHistoryResponse.from_orm(price)
        response.product_name = product.name if product else None
        response.competitor_name = competitor.name if competitor else None
        result.append(response)
    
    return result

@router.get("/stats/{product_id}")
async def get_price_stats(product_id: int, days: int = Query(30, ge=1), db: Session = Depends(get_db)):
    """Get price statistics for a product"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    prices = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id,
        PriceHistory.timestamp >= start_date
    ).all()
    
    if not prices:
        return {"error": "No price data found"}
    
    price_list = [p.price for p in prices]
    
    return {
        "product_id": product_id,
        "period_days": days,
        "average_price": sum(price_list) / len(price_list),
        "min_price": min(price_list),
        "max_price": max(price_list),
        "price_count": len(price_list),
        "price_range": max(price_list) - min(price_list)
    }

