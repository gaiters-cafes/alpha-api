import requests
from pydantic import BaseModel, Field
from typing import List
from fastapi import HTTPException
from .logging import logger

class AlphaVantageClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        logger.info("AlphaVantageClient initialised.")

    def get_commodities(self, function: str, interval: str) -> dict:
        params = {
            "function": function,
            "interval": interval,
            "apikey": self.api_key
        }
        logger.info(f"Making request to Alpha Vantage with params: {params}")
        response = requests.get(self.base_url, params=params)

        if response.status_code != 200:
            logger.error(f"Request failed with status code {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="API request failed.")
        
        data = response.json()
        logger.debug(f"Response received: {data}")
        
        if "Error Message" in data:
            logger.error(f"API error: {data['Error Message']}")
            raise HTTPException(status_code=400, detail=data["Error Message"])
        
        logger.info("Data successfully retrieved from Alpha Vantage.")
        return data

class DataPoint(BaseModel):
    date: str = Field(..., json_schema_extra={"example": "2024-06-01"})
    value: str = Field(..., json_schema_extra={"example": "205.226054898333"})

class CommoditiesAPIResponse(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Global Price of Wheat"})
    interval: str = Field(..., json_schema_extra={"example": "monthly"})
    unit: str = Field(..., json_schema_extra={"example": "dollar per metric ton"})
    data: List[DataPoint] = Field(..., json_schema_extra={
        "example": [
            {
                "date": "2024-06-01",
                "value": "205.226054898333"
            },
            {
                "date": "2024-05-01",
                "value": "200.112234567890"
            }
        ]
    })