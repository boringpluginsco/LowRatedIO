from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.outscraper import get_negative_reviews, get_trustpilot_reviews
from app.google_places import get_low_rated_places
from app.apify_places import get_apify_low_rated_places
from app.trustpilot import get_trustpilot_reviews
from app.serp_search import search_negative_mentions, format_results_for_ai
from app.ai_analyzer import analyze_reputation_data, get_risk_level_color, get_risk_level_bg
from urllib.parse import urlparse
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration"""
    return {"status": "healthy", "service": "LowRated"}

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search", response_class=HTMLResponse)
async def search(
    request: Request, 
    category: str = Form(...), 
    location: str = Form(...),
    api_choice: str = Form(...)
):
    query = f"{category} in {location}"
    
    if api_choice == "outscraper":
        businesses = await get_negative_reviews(query)
    elif api_choice == "google_places":
        businesses = await get_low_rated_places(query)
    elif api_choice == "apify":
        businesses = await get_apify_low_rated_places(category, location)
    else:
        businesses = []
    
    return templates.TemplateResponse("results.html", {"request": request, "results": businesses}) 

@app.get("/trustpilot-reviews")
async def trustpilot_reviews(domain: str = Query(...)):
    reviews = get_trustpilot_reviews(domain)
    return JSONResponse(content={"reviews": reviews}) 

@app.get("/api/trustpilot-reviews")
async def trustpilot_reviews(request: Request):
    url = request.query_params.get('url')
    if not url:
        return JSONResponse(content={"error": "URL parameter is required."}, status_code=400)
    reviews = get_trustpilot_reviews([url])
    return JSONResponse(content={"reviews": reviews})

@app.post("/api/ai-search")
async def ai_reputation_search(request: Request):
    """
    Perform AI-powered reputation analysis using SERP search and OpenAI analysis.
    """
    try:
        data = await request.json()
        domain = data.get('domain')
        
        if not domain:
            return JSONResponse(
                content={"error": "Domain parameter is required."}, 
                status_code=400
            )
        
        # Extract business name from domain
        parsed_domain = urlparse(domain if domain.startswith('http') else f'https://{domain}')
        business_name = parsed_domain.netloc.replace('www.', '').split('.')[0]
        
        # Get existing Trustpilot data if available
        trustpilot_reviews = get_trustpilot_reviews([domain])
        
        # Perform SERP search for negative mentions
        search_results = search_negative_mentions(business_name, limit=15)
        formatted_search_results = format_results_for_ai(search_results, business_name)
        
        # Analyze with AI
        ai_analysis = analyze_reputation_data(
            business_name=business_name,
            search_results=formatted_search_results,
            trustpilot_data=trustpilot_reviews
        )
        
        # Add UI styling classes
        ai_analysis['risk_color'] = get_risk_level_color(ai_analysis.get('risk_level', 'Unknown'))
        ai_analysis['risk_bg'] = get_risk_level_bg(ai_analysis.get('risk_level', 'Unknown'))
        ai_analysis['search_results'] = search_results
        ai_analysis['business_name'] = business_name
        
        return JSONResponse(content={
            "success": True,
            "analysis": ai_analysis,
            "search_count": len(search_results),
            "trustpilot_count": len(trustpilot_reviews) if trustpilot_reviews else 0
        })
        
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "error": f"AI search failed: {str(e)}"
            },
            status_code=500
        ) 