# 🛒 Shopping Assistant

A free shopping assistant that helps you find the average price and buying options for products or services in your zip code.

## Features

- ✅ Find average prices for any product or service
- ✅ Get a list of buying options (online and local stores)
- ✅ Price comparison across different retailers
- ✅ Personalized recommendations
- ✅ Uses OpenAI GPT-4 for intelligent responses
- ✅ Completely interactive CLI interface

## Installation

1. **Install Python 3.8+** (if not already installed)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key** (optional - already included in code):
   
   The API key is already configured in the code. If you prefer to use an environment variable instead:
   
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage

Run the shopping assistant:
```bash
python shopping_assistant.py
```

### Example Interaction:

```
What product or service are you looking for? iPhone 15
Enter your zip code: 10001

⏳ Searching for the best deals...

SHOPPING RESULTS
[Detailed price comparison and buying options...]
```

## How It Works

1. **Enter Product/Service**: Tell the assistant what you're looking for
2. **Enter Zip Code**: Provide your location for localized recommendations
3. **Get Results**: Receive average prices and a list of buying options
4. **Compare Prices**: See price ranges across different retailers
5. **Get Recommendations**: Get personalized suggestions based on value

## Free to Use

This assistant uses:
- **OpenAI API**: Powered by GPT-4 for intelligent product research
- **Zero additional costs**: No third-party shopping API fees required

## Notes

- The assistant uses AI to provide price estimates and recommendations
- Results are based on general market knowledge and data
- For highly specialized or rare items, results may vary
- Always verify actual prices on retailer websites

## Requirements

- Python 3.8+
- openai library
- OpenAI API key (included in code)

## Troubleshooting

If you encounter any issues:
1. Make sure you have Python 3.8+ installed
2. Install all dependencies: `pip install -r requirements.txt`
3. Check your internet connection
4. Verify the API key is valid

## License

Free to use and modify.


