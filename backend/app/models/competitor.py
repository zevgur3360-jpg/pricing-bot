"""
Competitor Model
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class CompetitorType(enum.Enum):
    ECOMMERCE = "ecommerce"
    MARKETPLACE = "marketplace"
    BRICK_MORTAR = "brick_mortar"
    HYBRID = "hybrid"

class Competitor(Base):
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    website = Column(String(500), nullable=False)
    type = Column(Enum(CompetitorType), default=CompetitorType.ECOMMERCE)
    description = Column(Text, nullable=True)
    logo_url = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    # price_history = relationship("PriceHistory", back_populates="competitor")


