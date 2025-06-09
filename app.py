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

@app.get("/api/weather")
async def get_weather(
    lat: float = Query(None),
    lon: float = Query(None),
    city: str = Query(None)
):
    try:
        logger.debug(f"Received request with lat: {lat}, lon: {lon}, city: {city}")
        
        if lat is not None and lon is not None:
            # Use coordinates if provided
            params = {
                'lat': lat,
                'lon': lon,
                'appid': API_KEY,
                'units': 'metric'
            }
            logger.debug(f"Using coordinates. Params: {params}")
        elif city:
            # Use city name if provided
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'
            }
            logger.debug(f"Using city name. Params: {params}")
        else:
            logger.error("No coordinates or city name provided")
            return {"error": "Either city name or coordinates (lat, lon) are required"}

        url = f"{BASE_URL}/weather"
        logger.debug(f"Making request to: {url}")
        response = requests.get(url, params=params)
        logger.debug(f"Response status code: {response.status_code}")
        
        data = response.json()
        logger.debug(f"Response data: {data}")

        if data.get('cod') != 200:
            error_message = data.get('message', 'City not found')
            logger.error(f"API error: {error_message}")
            if 'Invalid API key' in error_message:
                return {"error": "Weather service is currently unavailable. Please try again later."}
            return {"error": error_message}

        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return {"error": "Weather service is currently unavailable. Please try again later."}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"error": "Weather service is currently unavailable. Please try again later."}

@app.get("/api/forecast")
async def get_forecast(
    lat: float = Query(None),
    lon: float = Query(None),
    city: str = Query(None)
):
    try:
        logger.debug(f"Received forecast request with lat: {lat}, lon: {lon}, city: {city}")
        
        if lat is not None and lon is not None:
            # Use coordinates if provided
            params = {
                'lat': lat,
                'lon': lon,
                'appid': API_KEY,
                'units': 'metric'
            }
            logger.debug(f"Using coordinates. Params: {params}")
        elif city:
            # Use city name if provided
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'
            }
            logger.debug(f"Using city name. Params: {params}")
        else:
            logger.error("No coordinates or city name provided")
            return {"error": "Either city name or coordinates (lat, lon) are required"}

        url = f"{BASE_URL}/forecast"
        logger.debug(f"Making request to: {url}")
        response = requests.get(url, params=params)
        logger.debug(f"Response status code: {response.status_code}")
        
        data = response.json()
        logger.debug(f"Response data: {data}")

        if data.get('cod') != '200':
            error_message = data.get('message', 'City not found')
            logger.error(f"API error: {error_message}")
            if 'Invalid API key' in error_message:
                return {"error": "Weather service is currently unavailable. Please try again later."}
            return {"error": error_message}

        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return {"error": "Weather service is currently unavailable. Please try again later."}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"error": "Weather service is currently unavailable. Please try again later."}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get('PORT', 5001))
    uvicorn.run(app, host="0.0.0.0", port=port) 