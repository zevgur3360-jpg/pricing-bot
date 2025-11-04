"""
Price History Model - TimescaleDB Hypertable
Stores historical price data for time-series analysis
"""

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id"), nullable=False, index=True)
    price = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    availability = Column(Integer, default=1)  # 1 = in stock, 0 = out of stock
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    # Additional metadata
    sale_price = Column(Float, nullable=True)
    discount_percentage = Column(Float, nullable=True)
    promotion_active = Column(Integer, default=0)

    # Composite index for efficient time-series queries
    __table_args__ = (
        Index('idx_product_competitor_time', 'product_id', 'competitor_id', 'timestamp'),
    )

    # Relationships
    # product = relationship("Product", back_populates="price_history")
    # competitor = relationship("Competitor", back_populates="price_history")



