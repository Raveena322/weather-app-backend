from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
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
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    city: Optional[str] = Query(None)
):
    try:
        if not any([lat, lon, city]):
            raise HTTPException(status_code=400, detail="Either city name or coordinates (lat, lon) are required")

        params = {
            'appid': API_KEY,
            'units': 'metric'
        }

        if lat is not None and lon is not None:
            params.update({'lat': lat, 'lon': lon})
        elif city:
            params.update({'q': city})
        
        url = f"{BASE_URL}/weather"
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            error_data = response.json()
            raise HTTPException(
                status_code=response.status_code,
                detail=error_data.get('message', 'Weather service error')
            )

        return response.json()

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Weather service timeout")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="Weather service unavailable")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/forecast")
async def get_forecast(
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    city: Optional[str] = Query(None)
):
    try:
        if not any([lat, lon, city]):
            raise HTTPException(status_code=400, detail="Either city name or coordinates (lat, lon) are required")

        params = {
            'appid': API_KEY,
            'units': 'metric'
        }

        if lat is not None and lon is not None:
            params.update({'lat': lat, 'lon': lon})
        elif city:
            params.update({'q': city})
        
        url = f"{BASE_URL}/forecast"
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            error_data = response.json()
            raise HTTPException(
                status_code=response.status_code,
                detail=error_data.get('message', 'Weather service error')
            )

        return response.json()

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Weather service timeout")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="Weather service unavailable")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get('PORT', 5001))
    uvicorn.run(app, host="0.0.0.0", port=port) 