# Pricing Intelligence Platform - Backend

FastAPI backend with Ollama AI integration and SQLite database.

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python init_db.py
```

This creates the SQLite database file: `pricing_intelligence.db`

### 3. Run Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

API will be available at: http://localhost:8000

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Products
- `GET /api/products` - List all products
- `POST /api/products` - Create product
- `GET /api/products/{id}` - Get product details
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

### Competitors
- `GET /api/competitors` - List competitors
- `POST /api/competitors` - Create competitor
- `GET /api/competitors/{id}` - Get competitor details

### Prices
- `POST /api/prices` - Record price
- `GET /api/prices/product/{id}` - Get price history
- `GET /api/prices/compare?product_id={id}` - Compare prices
- `GET /api/prices/stats/{id}` - Get price statistics

### Analytics
- `GET /api/analytics/recommendation/{product_id}` - AI pricing recommendation
- `GET /api/analytics/insights?days=30` - Market insights
- `GET /api/analytics/competitor-analysis/{id}` - Competitor analysis

### Scraping
- `POST /api/scraping/scrape` - Scrape price from URL
- `POST /api/scraping/scrape-and-save` - Scrape and save to database

## Environment Variables

**Required:** Create `.env` file in the `backend/` directory:

```env
OLLAMA_API_KEY=your-ollama-api-key-here
DATABASE_URL=sqlite:///./pricing_intelligence.db
OLLAMA_API_URL=https://api.ollama.ai/v1/chat/completions
OLLAMA_MODEL=llama3.2
FRONTEND_URL=http://localhost:3000
```

**Important:** The `OLLAMA_API_KEY` is required. Copy `.env.example` to `.env` and add your API key.

You can copy the example file:
```bash
cp .env.example .env
# Then edit .env and add your OLLAMA_API_KEY
```

## Features

✅ RESTful API with FastAPI
✅ SQLite database (free, no setup required)
✅ Ollama AI integration for pricing recommendations
✅ Web scraping service
✅ Price history tracking
✅ Competitive intelligence
✅ Market analytics

## Next Steps

1. Add products and competitors
2. Start tracking prices
3. View analytics and AI recommendations
4. Use scraping service to collect prices

## Database Schema

- **products**: Product catalog
- **competitors**: Competitor information
- **price_history**: Historical price data
- **reviews**: Product reviews with sentiment
