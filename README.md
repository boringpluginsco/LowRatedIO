# LowRated

LowRated is an AI-powered web application that helps you discover and analyze businesses with negative reviews for reputation management opportunities. Find low-rated businesses by category and location, then get detailed AI analysis combining Trustpilot reviews and web search results.

## Features

- 🔍 **Multi-API Search**: Outscraper, Google Places, and Apify integration
- 🤖 **AI Analysis**: OpenAI-powered reputation analysis with SERP search
- 📊 **Trustpilot Integration**: Detailed review analysis and rating insights
- 🎨 **Modern UI**: Responsive design with glassmorphism effects
- ⚡ **Real-time Loading**: Interactive multi-stage loading experiences
- 📱 **Mobile Responsive**: Works seamlessly on all devices

## Quick Start

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd LowRatedIO
   ```

2. Copy environment variables:
   ```bash
   cp .env.example .env
   ```

3. Add your API keys to `.env`:
   ```env
   OUTSCRAPER_API_KEY=your_outscraper_api_key_here
   SERPAPI_KEY=your_serpapi_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here  # Optional
   APIFY_TOKEN=your_apify_token_here        # Optional
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

Visit `http://localhost:8000` to access the application.

## Docker Deployment

### Local Docker

```bash
# Build the image
docker build -t lowrated .

# Run the container
docker run -p 8000:8000 --env-file .env lowrated
```

### Docker Compose

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

## Coolify Deployment

### Prerequisites

1. A Coolify instance running on your server
2. Your code pushed to GitHub/GitLab
3. API keys for the required services

### Deployment Steps

1. **Connect Repository**:
   - In Coolify, create a new application
   - Connect your GitHub/GitLab repository
   - Select the main branch

2. **Configure Build**:
   - Build Pack: `Docker`
   - Dockerfile: `./Dockerfile`
   - Build Command: (leave default)
   - Start Command: (leave default)

3. **Environment Variables**:
   Set the following environment variables in Coolify:
   ```
   OUTSCRAPER_API_KEY=your_outscraper_api_key_here
   SERPAPI_KEY=your_serpapi_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here     # Optional
   APIFY_TOKEN=your_apify_token_here           # Optional
   ```

4. **Port Configuration**:
   - Application Port: `8000`
   - Health Check URL: `/health`

5. **Deploy**:
   - Click "Deploy" to start the deployment process
   - Monitor the build logs for any issues
   - Once deployed, test the health endpoint: `https://your-domain.com/health`

### Coolify Configuration Tips

- **Persistent Storage**: Not required for this application
- **Domain**: Configure your custom domain in Coolify settings
- **SSL**: Enable automatic SSL certificate generation
- **Scaling**: Start with 1 instance, scale as needed
- **Resource Limits**: 
  - Memory: 512MB minimum (1GB recommended)
  - CPU: 0.5 cores minimum

## API Requirements

### Required APIs
- **Outscraper API**: For business data and Trustpilot reviews
- **SERP API**: For web search functionality  
- **OpenAI API**: For AI-powered reputation analysis

### Optional APIs
- **Google Places API**: Alternative business search
- **Apify API**: Additional business data source

## Tech Stack

- **Frontend**: HTML, Tailwind CSS, Vanilla JavaScript
- **Backend**: Python (FastAPI)
- **AI**: OpenAI GPT-4
- **APIs**: Outscraper, SERP API, Trustpilot, Google Places, Apify
- **Deployment**: Docker, Coolify

## Architecture

```
User Request → FastAPI → API Integrations → AI Analysis → Response
                ↓
            Static Files (HTML/CSS/JS)
                ↓
            Business Search Results
                ↓
            AI-Powered Analysis Panel
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the logs: `docker-compose logs -f`
2. Verify API keys are correctly set
3. Test the health endpoint: `/health`
4. Review environment variable configuration 