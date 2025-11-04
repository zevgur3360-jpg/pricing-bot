# 🔒 Security Guide - API Keys

## Protecting Your API Keys

API keys have been removed from the codebase and must be set via environment variables.

## Setup Instructions

### Backend (.env file)

1. Create `.env` file in `backend/` directory:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. Edit `.env` and add your Ollama API key:
   ```env
   OLLAMA_API_KEY=your-actual-api-key-here
   ```

3. **Never commit `.env` to git** - it's already in `.gitignore`

### Frontend (.env.local file)

1. Create `.env.local` file in `web-app/` directory:
   ```bash
   cd web-app
   cp .env.example .env.local
   ```

2. Edit `.env.local` and add your Ollama API key:
   ```env
   OLLAMA_API_KEY=your-actual-api-key-here
   ```

3. **Never commit `.env.local` to git** - it's already in `.gitignore`

## Verification

### Backend
The backend will raise an error if `OLLAMA_API_KEY` is not set:
```python
ValueError: OLLAMA_API_KEY environment variable is required
```

### Frontend
The frontend will return an error if `OLLAMA_API_KEY` is not set:
```json
{"error": "OLLAMA_API_KEY environment variable is not configured"}
```

## Deployment

### Vercel (Frontend)
1. Go to Project Settings → Environment Variables
2. Add `OLLAMA_API_KEY` with your key
3. Add `NEXT_PUBLIC_API_URL` with your backend URL

### Backend Deployment
1. Set environment variable `OLLAMA_API_KEY` in your hosting platform
2. Never hardcode keys in production

## Best Practices

✅ **Do:**
- Use environment variables
- Keep `.env` files local only
- Use different keys for dev/staging/prod
- Rotate keys regularly

❌ **Don't:**
- Commit `.env` files to git
- Hardcode API keys in code
- Share API keys publicly
- Use the same key everywhere

## Troubleshooting

If you see errors about missing API keys:
1. Check that `.env` (backend) or `.env.local` (frontend) exists
2. Verify the key name is exactly `OLLAMA_API_KEY`
3. Restart your server after adding/updating environment variables



