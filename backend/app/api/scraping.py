"""
Scraping API Routes
Web scraping endpoints for price collection
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.services.scraper import PriceScraper
from app.models.product import Product
from app.models.competitor import Competitor
from app.models.price_history import PriceHistory
from datetime import datetime

router = APIRouter()
scraper = PriceScraper()

class ScrapeRequest(BaseModel):
    url: str
    product_id: Optional[int] = None
    competitor_id: Optional[int] = None

class ScrapeResponse(BaseModel):
    url: str
    price: Optional[float]
    product_info: dict
    success: bool

@router.post("/scrape", response_model=ScrapeResponse)
async def scrape_price_endpoint(request: ScrapeRequest, db: Session = Depends(get_db)):
    """Scrape price from a URL"""
    try:
        # Scrape price
        price = scraper.scrape_price(request.url)
        
        # Get product info
        product_info = scraper.get_product_info(request.url)
        
        # If product_id and competitor_id provided, save to database
        if request.product_id and request.competitor_id and price:
            product = db.query(Product).filter(Product.id == request.product_id).first()
            competitor = db.query(Competitor).filter(Competitor.id == request.competitor_id).first()
            
            if product and competitor:
                price_history = PriceHistory(
                    product_id=request.product_id,
                    competitor_id=request.competitor_id,
                    price=price,
                    timestamp=datetime.utcnow()
                )
                db.add(price_history)
                db.commit()
        
        return ScrapeResponse(
            url=request.url,
            price=price,
            product_info=product_info,
            success=price is not None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping error: {str(e)}")

@router.post("/scrape-and-save")
async def scrape_and_save(
    url: str,
    product_id: int,
    competitor_id: int,
    db: Session = Depends(get_db)
):
    """Scrape price and automatically save to database"""
    product = db.query(Product).filter(Product.id == product_id).first()
    competitor = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    
    price = scraper.scrape_price(url)
    
    if not price:
        raise HTTPException(status_code=400, detail="Could not extract price from URL")
    
    price_history = PriceHistory(
        product_id=product_id,
        competitor_id=competitor_id,
        price=price,
        timestamp=datetime.utcnow()
    )
    db.add(price_history)
    db.commit()
    
    return {
        "message": "Price scraped and saved successfully",
        "price": price,
        "product_id": product_id,
        "competitor_id": competitor_id
    }



