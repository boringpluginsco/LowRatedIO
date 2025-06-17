import os
from dotenv import load_dotenv
import logging
from outscraper import ApiClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

API_KEY = os.getenv("OUTSCRAPER_API_KEY")
client = ApiClient(api_key=API_KEY)

async def get_negative_reviews(query: str, limit: int = 5):
    """
    Get lowest-rated businesses matching the query using the reviews-v3 endpoint.
    """
    try:
        logger.info(f"Making API request to Outscraper with query: {query}")
        
        # Use the reviews-v3 endpoint with proper parameters
        results = client.google_maps_reviews(
            query,
            reviews_limit=5,  # Get 5 reviews per business
            limit=limit,      # Number of businesses to return
            sort="lowest_rating",  # Sort by lowest rating
            cutoff_rating=2,  # Only include businesses with rating below 4
            language="en",
            #reviews_query="the"
        )
        
        logger.info(f"Received results from API")
        
        if not results or not isinstance(results, list):
            logger.error(f"Invalid response format: {results}")
            return []
            
        businesses = []
        for place in results:
            if not place:
                continue
                
            business = {
                "name": place.get("name"),
                "address": place.get("full_address"),
                "rating": place.get("rating"),
                "reviews_count": place.get("reviews"),
                "website": place.get("site") or place.get("website") or place.get("domain"),
                "reviews": []
            }
            
            # Add reviews if available
            reviews_data = place.get("reviews_data", [])
            for review in reviews_data:
                business["reviews"].append({
                    "author": review.get("autor_name"),
                    "rating": review.get("review_rating"),
                    "text": review.get("review_text"),
                    "date": review.get("review_datetime_utc")
                })
            
            businesses.append(business)
        
        logger.info(f"Processed {len(businesses)} businesses")
        return businesses
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return [] 

async def get_trustpilot_reviews(domain: str, limit: int = 10):
    """
    Fetch reviews from Trustpilot for a given domain using Outscraper API.
    """
    try:
        logger.info(f"Fetching Trustpilot reviews for domain: {domain}")
        results = client.trustpilot_reviews(
            [domain],
            limit=limit,
            sort="recency",
            language="en",
            async_req=False
        )
        logger.info(f"Trustpilot API response: {results}")
        reviews = []
        if results and isinstance(results, list) and len(results) > 0:
            items = results[0].get("reviews_data", [])
            for review in items:
                reviews.append({
                    "author": review.get("author"),
                    "rating": review.get("rating"),
                    "text": review.get("text"),
                    "date": review.get("date")
                })
        return reviews
    except Exception as e:
        logger.error(f"Trustpilot error: {str(e)}")
        return [] 