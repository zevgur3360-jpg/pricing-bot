"""
Ollama API Service
Integration with Ollama for AI-powered features
"""

import os
import httpx
from typing import Optional, Dict, List
from dotenv import load_dotenv

load_dotenv()

class OllamaService:
    """Service for interacting with Ollama API"""
    
    def __init__(self):
        self.api_key = os.getenv("OLLAMA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OLLAMA_API_KEY environment variable is required. "
                "Please set it in your .env file or environment."
            )
        self.api_url = os.getenv(
            "OLLAMA_API_URL",
            "https://api.ollama.ai/v1/chat/completions"
        )
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1500
    ) -> Optional[str]:
        """Generate response using Ollama"""
        try:
            messages = []
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}"
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content") or data.get("response")
        except Exception as e:
            print(f"Ollama API error: {str(e)}")
            return None
    
    async def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of text"""
        prompt = f"""Analyze the sentiment of this review text and return JSON with:
- sentiment: "positive", "negative", or "neutral"
- score: number between -1 and 1
- confidence: number between 0 and 1

Text: {text}

Return only valid JSON."""
        
        system_prompt = "You are a sentiment analysis expert. Return only valid JSON."
        
        response = await self.generate_response(prompt, system_prompt, temperature=0.3)
        
        if response:
            try:
                import json
                # Try to extract JSON from response
                json_str = response.strip()
                if json_str.startswith("```"):
                    json_str = json_str.split("```")[1]
                    if json_str.startswith("json"):
                        json_str = json_str[4:]
                    json_str = json_str.strip()
                return json.loads(json_str)
            except:
                # Fallback sentiment analysis
                text_lower = text.lower()
                positive_words = ["good", "great", "excellent", "love", "amazing", "perfect", "best"]
                negative_words = ["bad", "terrible", "awful", "hate", "worst", "poor", "disappointed"]
                
                pos_count = sum(1 for word in positive_words if word in text_lower)
                neg_count = sum(1 for word in negative_words if word in text_lower)
                
                if pos_count > neg_count:
                    return {"sentiment": "positive", "score": 0.5, "confidence": 0.7}
                elif neg_count > pos_count:
                    return {"sentiment": "negative", "score": -0.5, "confidence": 0.7}
                else:
                    return {"sentiment": "neutral", "score": 0.0, "confidence": 0.5}
        
        return {"sentiment": "neutral", "score": 0.0, "confidence": 0.5}
    
    async def generate_pricing_recommendation(
        self,
        product_name: str,
        current_price: float,
        competitor_prices: List[float],
        market_data: Optional[Dict] = None
    ) -> Dict:
        """Generate AI-powered pricing recommendation"""
        competitors_str = ", ".join([f"${p:.2f}" for p in competitor_prices])
        avg_competitor = sum(competitor_prices) / len(competitor_prices) if competitor_prices else current_price
        
        prompt = f"""As a pricing intelligence expert, analyze this pricing situation:

Product: {product_name}
Current Price: ${current_price:.2f}
Competitor Prices: {competitors_str}
Average Competitor Price: ${avg_competitor:.2f}

Provide pricing recommendations in JSON format with:
- recommended_price: optimal price
- strategy: "competitive", "premium", or "value"
- reasoning: brief explanation
- confidence: 0-1 score

Return only valid JSON."""
        
        system_prompt = "You are a pricing strategy expert. Return only valid JSON."
        
        response = await self.generate_response(prompt, system_prompt, temperature=0.5)
        
        if response:
            try:
                import json
                json_str = response.strip()
                if json_str.startswith("```"):
                    json_str = json_str.split("```")[1]
                    if json_str.startswith("json"):
                        json_str = json_str[4:]
                    json_str = json_str.strip()
                return json.loads(json_str)
            except:
                pass
        
        # Fallback recommendation
        if current_price > avg_competitor * 1.1:
            strategy = "value"
            recommended = avg_competitor * 0.95
        elif current_price < avg_competitor * 0.9:
            strategy = "premium"
            recommended = avg_competitor * 1.05
        else:
            strategy = "competitive"
            recommended = avg_competitor
        
        return {
            "recommended_price": round(recommended, 2),
            "strategy": strategy,
            "reasoning": f"Competitive pricing based on market average of ${avg_competitor:.2f}",
            "confidence": 0.75
        }

