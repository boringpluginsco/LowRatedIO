import os
import logging
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Outscraper API key
OUTSCRAPER_API_KEY = os.getenv('OUTSCRAPER_API_KEY')


def extract_domain(url):
    """Extract clean domain name from URL using urlparse."""
    parsed = urlparse(url)
    return parsed.netloc or parsed.path


def get_trustpilot_reviews(queries, limit=3, async_mode='false'):
    """
    Fetch reviews from Trustpilot using the Outscraper API.

    :param queries: List of Trustpilot URLs or domain names, or a single string.
    :param limit: Max reviews per query.
    :param async_mode: Whether to run async (default: 'false').
    :return: List of reviews or empty list.
    """
    headers = {
        'X-API-KEY': OUTSCRAPER_API_KEY
    }

    if isinstance(queries, str):
        queries = [queries]

    cleaned_queries = [extract_domain(q.strip()) for q in queries]

    # Correct param structure: multiple query parameters instead of comma-joined string
    params = [('query', q) for q in cleaned_queries]
    params.append(('limit', limit))
    params.append(('async', async_mode))

    try:
        logging.info(f"Making Trustpilot API request with params: {params}")
        response = requests.get(
            'https://api.outscraper.cloud/trustpilot/reviews',
            headers=headers,
            params=params
        )
        response.raise_for_status()
        data = response.json()

        logging.info(f"Raw Trustpilot API response: {data}")

        # Check that the response has expected nested structure
        if 'data' in data and isinstance(data['data'], list) and data['data']:
            reviews = data['data'][0]
            if isinstance(reviews, list) and reviews:
                logging.info(f"Fetched {len(reviews)} reviews from Outscraper.")
                return reviews

        logging.warning("No reviews data found in API response")
        return []

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP error during Trustpilot review fetch: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return []

