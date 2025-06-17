import os
from apify_client import ApifyClient
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_TOKEN")

async def get_apify_low_rated_places(category: str, location: str, max_results: int = 5, return_limit: int = 5):
    """
    Fetch businesses from Apify's compass/crawler-google-places actor, filter for rating <= 3.0, and return up to 5 structured results. Only crawl up to 5 places to minimize credit usage.
    """
    try:
        client = ApifyClient(APIFY_TOKEN)
        run_input = {
            "searchStringsArray": [category],
            "locationQuery": location,
            "maxCrawledPlacesPerSearch": max_results,
            "language": "en"
        }
        logger.info(f"Calling Apify actor with input: {run_input}")
        run = client.actor("compass/crawler-google-places").call(run_input=run_input)
        filtered_results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            score = item.get("totalScore", 5)
            if score and score <= 3.0:
                filtered_results.append({
                    "name": item.get("title"),
                    "address": item.get("address"),
                    "rating": score,
                    "reviews_count": item.get("reviewsCount"),
                    "phone": item.get("phone"),
                    "website": item.get("website"),
                    "reviews": []
                })
            if len(filtered_results) >= return_limit:
                break
        logger.info(f"Apify: {len(filtered_results)} low-rated places found (limited to {return_limit}).")
        return filtered_results
    except Exception as e:
        logger.error(f"Apify error: {str(e)}")
        return [] 