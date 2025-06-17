import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def analyze_reputation_data(business_name: str, search_results: str, trustpilot_data: list = None) -> dict:
    """
    Analyze reputation data using OpenAI to identify risks and provide insights.
    
    :param business_name: Name of the business being analyzed
    :param search_results: Formatted search results from SERP
    :param trustpilot_data: Optional Trustpilot review data
    :return: Dictionary with AI analysis results
    """
    if not client:
        logger.error("OpenAI API key not found in environment variables")
        return {
            "error": "OpenAI API key not configured",
            "summary": "Unable to perform AI analysis. Please check OpenAI API configuration.",
            "risk_level": "unknown",
            "key_issues": [],
            "recommendations": []
        }
    
    try:
        # Prepare the context for AI analysis
        context = f"Business Name: {business_name}\n\n"
        context += "=== WEB SEARCH RESULTS ===\n"
        context += search_results
        
        if trustpilot_data:
            context += "\n\n=== TRUSTPILOT REVIEWS ===\n"
            for review in trustpilot_data:
                context += f"Rating: {review.get('review_rating', 'N/A')}/5\n"
                context += f"Author: {review.get('author_title', 'Anonymous')}\n"
                context += f"Review: {review.get('review_text', '')}\n"
                context += f"Date: {review.get('review_datetime_utc', '')}\n\n"
        
        # Create the AI prompt
        system_prompt = """You are a professional reputation monitoring and risk assessment AI. 
        Your job is to analyze online mentions and reviews of businesses to identify potential reputation risks.
        
        Provide a comprehensive analysis that includes:
        1. Overall risk assessment (Low, Medium, High, Critical)
        2. Key reputation issues identified
        3. Specific concerning patterns or trends
        4. Actionable recommendations for the business
        5. A concise executive summary
        
        Be objective, factual, and focus on legitimate concerns while filtering out frivolous complaints."""
        
        user_prompt = f"""Please analyze the following reputation data for '{business_name}' and provide a detailed assessment:

{context}

Please structure your response as a JSON object with the following format:
{{
    "risk_level": "Low|Medium|High|Critical",
    "summary": "Brief executive summary of findings",
    "key_issues": ["list", "of", "main", "issues", "found"],
    "concerning_patterns": ["any", "recurring", "themes", "or", "patterns"],
    "recommendations": ["specific", "actionable", "recommendations"],
    "positive_aspects": ["any", "positive", "mentions", "or", "mitigating", "factors"],
    "source_breakdown": {{
        "web_mentions": "count and summary",
        "trustpilot_reviews": "count and summary"
    }}
}}"""

        logger.info(f"Sending reputation analysis request to OpenAI for {business_name}")
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1500,
            temperature=0.3  # Lower temperature for more consistent, factual responses
        )
        
        ai_response = response.choices[0].message.content
        logger.info(f"Received AI analysis for {business_name}")
        
        # Try to parse JSON response, fallback to text if needed
        try:
            import json
            result = json.loads(ai_response)
        except json.JSONDecodeError:
            # Fallback if AI doesn't return valid JSON
            result = {
                "risk_level": "Medium",
                "summary": ai_response[:500] + "..." if len(ai_response) > 500 else ai_response,
                "key_issues": ["Analysis provided in summary"],
                "concerning_patterns": [],
                "recommendations": ["Review detailed analysis in summary"],
                "positive_aspects": [],
                "source_breakdown": {
                    "web_mentions": "See summary for details",
                    "trustpilot_reviews": "See summary for details"
                }
            }
        
        return result
        
    except Exception as e:
        logger.error(f"Error during AI analysis for {business_name}: {e}")
        return {
            "error": str(e),
            "risk_level": "Unknown",
            "summary": f"Error occurred during AI analysis: {str(e)}",
            "key_issues": ["Analysis failed due to technical error"],
            "concerning_patterns": [],
            "recommendations": ["Contact support to resolve analysis issue"],
            "positive_aspects": [],
            "source_breakdown": {
                "web_mentions": "Analysis failed",
                "trustpilot_reviews": "Analysis failed"
            }
        }


def get_risk_level_color(risk_level: str) -> str:
    """
    Get CSS color class based on risk level.
    
    :param risk_level: Risk level string
    :return: CSS color class
    """
    risk_colors = {
        "Low": "text-green-400",
        "Medium": "text-yellow-400", 
        "High": "text-orange-400",
        "Critical": "text-red-400",
        "Unknown": "text-gray-400"
    }
    return risk_colors.get(risk_level, "text-gray-400")


def get_risk_level_bg(risk_level: str) -> str:
    """
    Get background color class based on risk level.
    
    :param risk_level: Risk level string
    :return: CSS background color class
    """
    risk_backgrounds = {
        "Low": "bg-green-900/20 border-green-500",
        "Medium": "bg-yellow-900/20 border-yellow-500",
        "High": "bg-orange-900/20 border-orange-500", 
        "Critical": "bg-red-900/20 border-red-500",
        "Unknown": "bg-gray-900/20 border-gray-500"
    }
    return risk_backgrounds.get(risk_level, "bg-gray-900/20 border-gray-500") 