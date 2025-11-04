"""
FastAPI Main Application
Pricing Intelligence Platform Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Pricing Intelligence Platform API",
    description="Backend API for price tracking, competitive intelligence, and dynamic pricing",
    version="1.0.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
        os.getenv("FRONTEND_URL", "http://localhost:3000"),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/")
async def root():
    return {"message": "Pricing Intelligence Platform API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "pricing-intelligence-api"}

# Import routers
from app.api import products, competitors, prices, analytics, scraping

app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(competitors.router, prefix="/api/competitors", tags=["competitors"])
app.include_router(prices.router, prefix="/api/prices", tags=["prices"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(scraping.router, prefix="/api/scraping", tags=["scraping"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

