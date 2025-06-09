from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API key from environment variable
API_KEY = os.getenv('WEATHER_API_KEY', '53aae698143f63798f6d0f23e4bc846b')
BASE_URL = "http://api.openweathermap.org/data/2.5"

@app.get("/")
async def root():
    return {"message": "Weather API is running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/weather")
async def get_weather(
    lat: float = Query(None),
    lon: float = Query(None),
    city: str = Query(None)
):
    try:
        logger.debug(f"Received request with lat: {lat}, lon: {lon}, city: {city}")
        
        if lat is not None and lon is not None:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': API_KEY,
                'units': 'metric'
            }
        elif city:
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'
            }
        else:
            return {"error": "Either city name or coordinates (lat, lon) are required"}

        url = f"{BASE_URL}/weather"
        response = requests.get(url, params=params)
        data = response.json()

        if data.get('cod') != 200:
            error_message = data.get('message', 'City not found')
            return {"error": error_message}

        return data

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {"error": "Weather service is currently unavailable. Please try again later."}

@app.get("/api/forecast")
async def get_forecast(
    lat: float = Query(None),
    lon: float = Query(None),
    city: str = Query(None)
):
    try:
        if lat is not None and lon is not None:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': API_KEY,
                'units': 'metric'
            }
        elif city:
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'
            }
        else:
            return {"error": "Either city name or coordinates (lat, lon) are required"}

        url = f"{BASE_URL}/forecast"
        response = requests.get(url, params=params)
        data = response.json()

        if data.get('cod') != '200':
            error_message = data.get('message', 'City not found')
            return {"error": error_message}

        return data

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {"error": "Weather service is currently unavailable. Please try again later."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get('PORT', 5001))
    uvicorn.run(app, host="0.0.0.0", port=port) 