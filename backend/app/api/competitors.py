"""
Competitors API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.competitor import Competitor, CompetitorType
from datetime import datetime

router = APIRouter()

class CompetitorCreate(BaseModel):
    name: str
    website: str
    type: Optional[str] = "ecommerce"
    description: Optional[str] = None
    logo_url: Optional[str] = None

class CompetitorResponse(BaseModel):
    id: int
    name: str
    website: str
    type: str
    description: Optional[str]
    logo_url: Optional[str]
    is_active: int
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/", response_model=CompetitorResponse)
async def create_competitor(competitor: CompetitorCreate, db: Session = Depends(get_db)):
    """Create a new competitor"""
    competitor_type = CompetitorType[competitor.type.upper()] if competitor.type else CompetitorType.ECOMMERCE
    db_competitor = Competitor(
        name=competitor.name,
        website=competitor.website,
        type=competitor_type,
        description=competitor.description,
        logo_url=competitor.logo_url
    )
    db.add(db_competitor)
    db.commit()
    db.refresh(db_competitor)
    return db_competitor

@router.get("/", response_model=List[CompetitorResponse])
async def get_competitors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get list of competitors"""
    query = db.query(Competitor)
    
    if active_only:
        query = query.filter(Competitor.is_active == 1)
    
    competitors = query.offset(skip).limit(limit).all()
    return competitors

@router.get("/{competitor_id}", response_model=CompetitorResponse)
async def get_competitor(competitor_id: int, db: Session = Depends(get_db)):
    """Get a specific competitor by ID"""
    competitor = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return competitor



