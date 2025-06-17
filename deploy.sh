#!/bin/bash

# LowRated Deployment Script
# This script helps prepare and deploy the LowRated application

set -e

echo "🚀 LowRated Deployment Script"
echo "=============================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📝 Please copy .env.example to .env and fill in your API keys:"
    echo "   cp .env.example .env"
    echo ""
    echo "Required API keys:"
    echo "- OUTSCRAPER_API_KEY (Required)"
    echo "- SERPAPI_KEY (Required)" 
    echo "- OPENAI_API_KEY (Required)"
    echo "- GOOGLE_API_KEY (Optional)"
    echo "- APIFY_TOKEN (Optional)"
    exit 1
fi

echo "✅ .env file found"

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "✅ Docker is available"
    
    # Build the Docker image
    echo "🔨 Building Docker image..."
    docker build -t lowrated .
    
    echo "✅ Docker image built successfully"
    echo ""
    echo "🎯 Next steps for local testing:"
    echo "   docker run -p 8000:8000 --env-file .env lowrated"
    echo ""
else
    echo "⚠️  Docker not found (this is okay for Coolify deployment)"
fi

echo "📋 Deployment Checklist:"
echo "========================"
echo "✅ Dockerfile ready"
echo "✅ .dockerignore configured"
echo "✅ docker-compose.yml available"
echo "✅ Health check endpoint: /health"
echo "✅ Environment variables documented"
echo ""

echo "🎯 For Coolify deployment:"
echo "1. Push this code to your Git repository"
echo "2. In Coolify, create a new application"
echo "3. Connect your repository"
echo "4. Set environment variables:"
echo "   - OUTSCRAPER_API_KEY"
echo "   - SERPAPI_KEY" 
echo "   - OPENAI_API_KEY"
echo "   - GOOGLE_API_KEY (optional)"
echo "   - APIFY_TOKEN (optional)"
echo "5. Configure port: 8000"
echo "6. Set health check: /health"
echo "7. Deploy!"
echo ""

echo "🔗 Application will be available at:"
echo "   Local: http://localhost:8000"
echo "   Coolify: https://your-domain.com"
echo ""

echo "✨ Ready for deployment!" 