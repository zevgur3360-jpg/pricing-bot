"""
Product Model
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    sku = Column(String(100), unique=True, index=True)
    category = Column(String(100), index=True)
    brand = Column(String(100), index=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    base_price = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    # price_history = relationship("PriceHistory", back_populates="product")
    # reviews = relationship("Review", back_populates="product")



