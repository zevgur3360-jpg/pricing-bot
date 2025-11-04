#!/bin/bash
# Setup script for backend environment variables

echo "🔧 Setting up backend environment variables..."

if [ -f .env ]; then
    echo "⚠️  .env file already exists. Skipping..."
else
    cat > .env << EOF
# Ollama API Configuration (REQUIRED)
OLLAMA_API_KEY=your-ollama-api-key-here

# Ollama Settings
OLLAMA_API_URL=https://api.ollama.ai/v1/chat/completions
OLLAMA_MODEL=llama3.2

# Database Configuration
DATABASE_URL=sqlite:///./pricing_intelligence.db

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000
EOF
    echo "✅ Created .env file"
    echo "⚠️  IMPORTANT: Edit .env and add your OLLAMA_API_KEY!"
fi



