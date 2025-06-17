import os
import logging
import serpapi
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SerpAPI key
SERPAPI_KEY = os.getenv('SERPAPI_KEY')


def search_negative_mentions(business_name: str, limit: int = 10):
    """
    Search for negative mentions, reviews, and complaints about a business.
    
    :param business_name: Name of the business to search for
    :param limit: Maximum number of results to return
    :return: List of search results with negative mentions
    """
    if not SERPAPI_KEY:
        logger.error("SERPAPI_KEY not found in environment variables")
        return []
        
    try:
        # Search queries for negative mentions
        search_queries = [
            f'"{business_name}" negative reviews',
            f'"{business_name}" complaints',
            f'"{business_name}" scam',
            f'"{business_name}" bad service',
            f'"{business_name}" fraud'
        ]
        
        all_results = []
        
        for query in search_queries:
            logger.info(f"Searching: {query}")
            
            params = {
                "q": query,
                "api_key": SERPAPI_KEY,
                "num": min(limit // len(search_queries) + 2, 10),  # Distribute results across queries
                "gl": "us",  # Country
                "hl": "en",   # Language
                "engine": "google"  # Specify Google search engine
            }
            
            results = serpapi.search(params)
            
            # Extract organic results
            organic_results = results.get("organic_results", [])
            
            for result in organic_results:
                result_data = {
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                    "search_query": query,
                    "source": result.get("source", "")
                }
                
                # Filter for potentially negative content
                if is_potentially_negative(result_data):
                    all_results.append(result_data)
                    
                if len(all_results) >= limit:
                    break
                    
            if len(all_results) >= limit:
                break
                
        logger.info(f"Found {len(all_results)} potentially negative results for {business_name}")
        return all_results[:limit]
        
    except Exception as e:
        logger.error(f"Error during SERP search for {business_name}: {e}")
        return []


def is_potentially_negative(result_data: dict) -> bool:
    """
    Check if a search result potentially contains negative content.
    
    :param result_data: Dictionary containing search result data
    :return: True if potentially negative, False otherwise
    """
    negative_keywords = [
        'complaint', 'scam', 'fraud', 'terrible', 'awful', 'worst', 'horrible',
        'bad', 'negative', 'poor', 'disappointing', 'unprofessional', 'rude',
        'dishonest', 'avoid', 'warning', 'beware', 'lawsuit', 'legal action',
        'refund', 'money back', 'rip off', 'ripoff', 'stolen', 'theft'
    ]
    
    # Check title and snippet for negative keywords
    text_to_check = (result_data.get("title", "") + " " + result_data.get("snippet", "")).lower()
    
    return any(keyword in text_to_check for keyword in negative_keywords)


def format_results_for_ai(results: list, business_name: str) -> str:
    """
    Format search results for AI analysis.
    
    :param results: List of search results
    :param business_name: Name of the business
    :return: Formatted string for AI input
    """
    if not results:
        return f"No negative mentions found for {business_name} in web search."
    
    formatted_text = f"Web search results for negative mentions of '{business_name}':\n\n"
    
    for i, result in enumerate(results, 1):
        formatted_text += f"{i}. **{result['title']}**\n"
        formatted_text += f"   Source: {result['link']}\n"
        formatted_text += f"   Content: {result['snippet']}\n"
        formatted_text += f"   Search Query: {result['search_query']}\n\n"
    
    return formatted_text 