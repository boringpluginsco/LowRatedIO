import os
import httpx
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

async def get_low_rated_places(query: str, limit: int = 20):
    """
    Get businesses using the new Google Places API (v1). Show all results, no rating filter.
    """
    try:
        logger.info(f"Making API request to Google Places (New) with query: {query}")

        url = "https://places.googleapis.com/v1/places:searchText"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.userRatingCount"
        }
        data = {
            "textQuery": query,
            "pageSize": limit
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            result = response.json()
        logger.info(f"Raw Google Places API response: {result}")

        if "error" in result:
            logger.error(f"Google Places API error: {result['error'].get('message')}")
            return []

        # Parse all results (no filtering)
        places = result.get("places", [])
        logger.info(f"Number of places returned from Google: {len(places)}")
        all_places = [
            {
                "name": place.get("displayName", {}).get("text"),
                "address": place.get("formattedAddress"),
                "rating": place.get("rating"),
                "reviews_count": place.get("userRatingCount"),
                "reviews": []
            }
            for place in places
        ]
        logger.info(f"All places to be shown: {all_places}")

        return all_places

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return [] 