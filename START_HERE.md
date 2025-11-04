# 🚀 Pricing Intelligence Platform - Quick Start Guide

Complete platform with Ollama AI, SQLite database, and full-stack architecture.

## 🎯 What's Built

### ✅ Backend (FastAPI)
- RESTful API with full CRUD operations
- SQLite database (free, no setup needed)
- Ollama AI integration for pricing recommendations
- Web scraping service
- Price history tracking
- Competitive intelligence analytics

### ✅ Frontend (Next.js)
- Beautiful dashboard with analytics
- Products management
- Competitors tracking
- Price comparison views
- Market insights & charts
- AI-powered recommendations

## 🏃 Quick Start

### Step 1: Start Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Start server
uvicorn app.main:app --reload --port 8000
```

Backend will run at: **http://localhost:8000**
API Docs: **http://localhost:8000/docs**

### Step 2: Start Frontend

```bash
cd web-app

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at: **http://localhost:3000**

## 📋 First Steps

1. **Add Products**
   - Go to http://localhost:3000/products
   - Click "Add Product"
   - Enter product details

2. **Add Competitors**
   - Use API: `POST /api/competitors`
   - Or add via API docs at http://localhost:8000/docs

3. **Track Prices**
   - Use scraping API: `POST /api/scraping/scrape-and-save`
   - Or manually: `POST /api/prices`

4. **View Analytics**
   - Dashboard: http://localhost:3000/dashboard
   - Analytics: http://localhost:3000/analytics
   - Product details with AI recommendations

## 🔧 Configuration

### Backend Environment (.env in backend/)
**Required:** Create `.env` file in `backend/` directory:

```env
OLLAMA_API_KEY=your-ollama-api-key-here
DATABASE_URL=sqlite:///./pricing_intelligence.db
OLLAMA_API_URL=https://api.ollama.ai/v1/chat/completions
OLLAMA_MODEL=llama3.2
FRONTEND_URL=http://localhost:3000
```

Copy the example file:
```bash
cd backend
cp .env.example .env
# Edit .env and add your OLLAMA_API_KEY
```

### Frontend Environment (.env.local in web-app/)
**Required:** Create `.env.local` file in `web-app/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
OLLAMA_API_KEY=your-ollama-api-key-here
OLLAMA_API_URL=https://api.ollama.ai/v1/chat/completions
OLLAMA_MODEL=llama3.2
```

Copy the example file:
```bash
cd web-app
cp .env.example .env.local
# Edit .env.local and add your OLLAMA_API_KEY
```

## 📁 Project Structure

```
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── models/      # Database models
│   │   └── services/    # Business logic
│   └── init_db.py       # Initialize database
│
└── web-app/             # Next.js frontend
    ├── app/
    │   ├── dashboard/   # Dashboard page
    │   ├── products/    # Products pages
    │   └── analytics/   # Analytics page
    └── lib/
        └── api.ts       # API client
```

## 🎨 Features

### API Endpoints

**Products**
- `GET /api/products` - List products
- `POST /api/products` - Create product
- `GET /api/products/{id}` - Get product details

**Competitors**
- `GET /api/competitors` - List competitors
- `POST /api/competitors` - Create competitor

**Prices**
- `POST /api/prices` - Record price
- `GET /api/prices/product/{id}` - Price history
- `GET /api/prices/compare` - Compare prices

**Analytics**
- `GET /api/analytics/recommendation/{id}` - AI pricing recommendation
- `GET /api/analytics/insights` - Market insights

**Scraping**
- `POST /api/scraping/scrape` - Scrape price from URL

### Frontend Pages

- `/` - Home page with search
- `/dashboard` - Main dashboard
- `/products` - Products list
- `/products/new` - Add product
- `/products/[id]` - Product details with charts
- `/analytics` - Market analytics

## 🧪 Testing

### Test API

```bash
# Health check
curl http://localhost:8000/health

# Get products
curl http://localhost:8000/api/products

# Create product
curl -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "iPhone 15", "category": "Electronics", "base_price": 999.99}'
```

### Test Frontend

1. Open http://localhost:3000
2. Navigate to Dashboard
3. Add a product
4. View analytics

## 📊 Database

SQLite database file: `backend/pricing_intelligence.db`

Tables:
- `products` - Product catalog
- `competitors` - Competitor information
- `price_history` - Historical price data
- `reviews` - Product reviews

## 🚀 Deployment

### Backend (PythonAnywhere, Railway, etc.)
1. Set environment variables
2. Run: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Frontend (Vercel)
1. Push to GitHub
2. Import to Vercel
3. Set `NEXT_PUBLIC_API_URL` to your backend URL

## 🎉 Next Steps

1. Add real products and competitors
2. Set up automated scraping
3. Track prices over time
4. Use AI recommendations
5. Analyze market trends

## 📚 Documentation

- Backend API Docs: http://localhost:8000/docs
- Implementation Plan: `IMPLEMENTATION_PLAN.md`
- PRD: `web-app/pricing-intelligence-prd.pdf`

---

**Ready to build your pricing intelligence platform!** 🚀

