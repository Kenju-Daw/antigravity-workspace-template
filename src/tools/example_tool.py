import requests

def web_search(query: str) -> str:
    """Performs a web search for the given query.

    This is a mock function to demonstrate the expected structure of a tool.
    In a real implementation, this would call a search API like Google Custom Search
    or Serper.dev.

    Args:
        query: The search query string.

    Returns:
        A string containing the search results (mocked for this example).
    """
    # <thought>
    # In a real scenario, I would:
    # 1. Validate the query (ensure it's not empty).
    # 2. Construct the API request with proper headers and API key.
    # 3. Handle potential network errors or rate limits.
    # 4. Parse the JSON response to extract relevant snippets.
    # For now, I will return a placeholder string.
    # </thought>
    
    print(f"DEBUG: Performing web search for '{query}'")
    
    # Mock response
    results = f"Search results for: {query}\n1. Result A for {query}...\n2. Result B for {query}..."
    return results

def get_stock_price(ticker: str) -> float:
    """Retrieves the current stock price for a given ticker.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'GOOGL').
        
    Returns:
        The current price as a float.
    """
    # <thought>
    # This tool would typically connect to a financial data provider.
    # I need to ensure the ticker is uppercase.
    # </thought>
    
    print(f"DEBUG: Getting stock price for '{ticker}'")
    return 150.00 # Mock price
