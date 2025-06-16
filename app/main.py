from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.outscraper import get_negative_reviews
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, category: str = Form(...), location: str = Form(...)):
    query = f"{category} in {location}"
    businesses = await get_negative_reviews(query)
    return templates.TemplateResponse("results.html", {"request": request, "results": businesses}) 