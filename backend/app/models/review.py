"""
Review Model - Stores product reviews with sentiment analysis
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class SentimentType(enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id"), nullable=True, index=True)
    source = Column(String(50), nullable=False)  # google, yelp, amazon, etc.
    rating = Column(Float, nullable=False)
    content = Column(Text, nullable=True)
    sentiment = Column(Enum(SentimentType), nullable=True)
    sentiment_score = Column(Float, nullable=True)  # -1 to 1
    author = Column(String(255), nullable=True)
    review_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    # product = relationship("Product", back_populates="reviews")


