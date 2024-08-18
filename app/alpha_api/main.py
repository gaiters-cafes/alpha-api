
from fastapi import FastAPI, Query, HTTPException
from typing import Optional
import requests
from alpha_api.av_client import AlphaVantageClient, CommoditiesAPIResponse
from .config import Settings
from .logging import logger

# Load settings
settings = Settings()

app = FastAPI(
    title="Alpha Vantage API",
    description="This API is a wrapper over the alpha vantage api, which commodities such as crude oil, natural gas, copper, wheat, etc.(daily, weekly, monthly, quarterly, etc.)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

@app.get(
    "/get_commodities", 
    summary="Retrieve Commodities Data from Alpha Vantage", 
    description="Fetches commodities data from Alpha Vantage based on function and interval.",
    response_model=CommoditiesAPIResponse
)
def get_commodities(
    function: str = Query(..., description="Function type for the API query (e.g., 'WHEAT', 'COTTON', 'SUGAR')."),
    interval: str = Query(..., description="Interval for the data (e.g., 'monthly', 'quarterly', and 'annual').")
):
    """
    Fetch data from the Alpha Vantage API based on the function and interval.
    
    - **function**: The function type for the API query (e.g., 'WHEAT', 'COTTON', 'SUGAR').
    - **interval**: The interval for the data (e.g., 'monthly', 'quarterly', and 'annual').
    """
    try:
        logger.info("Attempting to request data from Alpha Vantage Commodities API.")
        api_client = AlphaVantageClient(api_key=settings.api_key)
        data = api_client.get_commodities(function=function, interval=interval)
        return data
    except HTTPException as e:
        logger.error(f"Error in endpoint: {e.detail}")
        raise e
