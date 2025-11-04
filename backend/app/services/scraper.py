"""
Web Scraping Service
Basic foundation for price scraping
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, List
import time
import random
from urllib.parse import urljoin, urlparse

class PriceScraper:
    """Basic web scraper for price extraction"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    
    def scrape_price(self, url: str, selectors: Optional[Dict[str, str]] = None) -> Optional[float]:
        """
        Scrape price from a URL
        
        Args:
            url: URL to scrape
            selectors: Optional dict with CSS selectors for price extraction
        
        Returns:
            Price as float or None
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try common price selectors if not provided
            if not selectors:
                selectors = [
                    '[data-price]',
                    '.price',
                    '.product-price',
                    '[class*="price"]',
                    '[itemprop="price"]',
                ]
            
            # Try to find price
            price_text = None
            if isinstance(selectors, dict):
                for selector_type, selector in selectors.items():
                    element = soup.select_one(selector)
                    if element:
                        price_text = element.get_text(strip=True)
                        break
            else:
                for selector in selectors:
                    element = soup.select_one(selector)
                    if element:
                        price_text = element.get_text(strip=True)
                        break
            
            if price_text:
                # Extract numeric value
                price = self._extract_price(price_text)
                return price
            
            return None
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
    
    def _extract_price(self, text: str) -> Optional[float]:
        """Extract numeric price from text"""
        import re
        # Remove currency symbols and extract numbers
        price_match = re.search(r'[\d,]+\.?\d*', text.replace(',', ''))
        if price_match:
            try:
                return float(price_match.group().replace(',', ''))
            except ValueError:
                return None
        return None
    
    def scrape_multiple_urls(self, urls: List[str], delay: float = 1.0) -> List[Dict]:
        """Scrape multiple URLs with delay"""
        results = []
        for url in urls:
            price = self.scrape_price(url)
            results.append({
                'url': url,
                'price': price,
                'timestamp': time.time()
            })
            time.sleep(delay + random.uniform(0, 0.5))  # Random delay
        return results
    
    def get_product_info(self, url: str) -> Dict:
        """Get basic product information from URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to extract title
            title = None
            title_selectors = ['h1', '[itemprop="name"]', '.product-title', 'title']
            for selector in title_selectors:
                element = soup.select_one(selector)
                if element:
                    title = element.get_text(strip=True)
                    break
            
            # Try to extract image
            image = None
            img_selectors = ['[itemprop="image"]', '.product-image img', 'img[src*="product"]']
            for selector in img_selectors:
                element = soup.select_one(selector)
                if element:
                    image = element.get('src') or element.get('data-src')
                    if image:
                        image = urljoin(url, image)
                    break
            
            return {
                'title': title or 'Unknown Product',
                'image': image,
                'url': url
            }
        except Exception as e:
            print(f"Error getting product info: {str(e)}")
            return {
                'title': 'Unknown Product',
                'image': None,
                'url': url
            }



