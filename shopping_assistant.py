#!/usr/bin/env python3
"""
Shopping Assistant - Find average prices and buying options for products in your zip code
"""

import os
import sys
from openai import OpenAI
from typing import List, Dict

class ShoppingAssistant:
    def __init__(self, api_key: str):
        """Initialize the shopping assistant with OpenAI API key"""
        self.client = OpenAI(api_key=api_key)
    
    def get_shopping_info(self, product: str, zip_code: str) -> str:
        """
        Get shopping information for a product in a specific zip code
        
        Args:
            product: Name of the product or service
            zip_code: Zip code to search in
            
        Returns:
            Formatted shopping information
        """
        
        prompt = f"""You are a shopping assistant. A user is looking for '{product}' in zip code {zip_code}.

Please provide:
1. Average price range for this product/service
2. List of 5-10 buying options (include online retailers, local stores if relevant, etc.)
3. Price comparison for each option
4. Recommendations based on value

Format your response clearly with sections. Be helpful and informative.

Note: If this is a product that requires local service (like a haircut, home repair), adjust recommendations accordingly."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful shopping assistant that provides price comparisons and buying options for products and services."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error getting shopping information: {str(e)}"
    
    def interactive_mode(self):
        """Run the assistant in interactive mode"""
        print("=" * 60)
        print("🛒 Shopping Assistant - Find Best Deals!")
        print("=" * 60)
        print("\nWelcome! I'll help you find the average price and buying options.")
        print("Enter 'quit' to exit.\n")
        
        while True:
            try:
                # Get product name
                product = input("What product or service are you looking for? ").strip()
                
                if product.lower() in ['quit', 'exit', 'q']:
                    print("\nThanks for using Shopping Assistant! Goodbye! 🛍️")
                    break
                
                if not product:
                    print("Please enter a product or service name.")
                    continue
                
                # Get zip code
                zip_code = input("Enter your zip code: ").strip()
                
                if not zip_code:
                    print("Please enter a valid zip code.")
                    continue
                
                print("\n⏳ Searching for the best deals...\n")
                
                # Get shopping info
                result = self.get_shopping_info(product, zip_code)
                
                print("=" * 60)
                print("SHOPPING RESULTS")
                print("=" * 60)
                print(result)
                print("=" * 60)
                print()
                
                # Ask if user wants to search again
                again = input("Would you like to search for another product? (yes/no): ").strip().lower()
                if again not in ['yes', 'y']:
                    print("\nThanks for using Shopping Assistant! Goodbye! 🛍️")
                    break
                print()
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user.")
                print("Thanks for using Shopping Assistant! Goodbye! 🛍️")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {str(e)}\n")


def main():
    """Main entry point"""
    # Use the API key from environment variable if set, otherwise use the provided one
    api_key = os.getenv('OPENAI_API_KEY', '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')
    
    if not api_key:
        print("Error: OpenAI API key not found!")
        print("Please set the OPENAI_API_KEY environment variable or modify the code.")
        sys.exit(1)
    
    # Create and run the shopping assistant
    assistant = ShoppingAssistant(api_key)
    assistant.interactive_mode()


if __name__ == "__main__":
    main()



