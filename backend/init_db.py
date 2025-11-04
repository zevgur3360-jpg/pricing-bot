"""
Initialize Database
Creates all tables
"""

from app.database import Base, engine
from app.models.product import Product
from app.models.competitor import Competitor
from app.models.price_history import PriceHistory
from app.models.review import Review

def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")
    print("Database file: pricing_intelligence.db")

if __name__ == "__main__":
    init_db()

