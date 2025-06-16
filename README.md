# RepScout

RepScout is a web application that helps you find businesses with negative reviews in a specific category and location using the Outscraper API.

## Features

- Search for businesses by category and location
- View businesses sorted by lowest ratings
- Clean and responsive UI using Tailwind CSS
- FastAPI backend for high performance
- Docker support for easy deployment

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and add your Outscraper API key:
   ```bash
   cp .env.example .env
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t repscout .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env repscout
   ```

## Deployment with Coolify

1. Push your code to GitHub/GitLab
2. Connect your repository in Coolify
3. Set the `OUTSCRAPER_API_KEY` environment variable in Coolify
4. Deploy the application

## Tech Stack

- Frontend: HTML + Tailwind CSS
- Backend: Python (FastAPI)
- API: Outscraper
- Deployment: Docker + Coolify 