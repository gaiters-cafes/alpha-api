import pytest
from fastapi.testclient import TestClient
from alpha_api.main import app
from alpha_api.config import Settings

client = TestClient(app)
settings = Settings()

def test_get_commodities_success():
    import os
    os.environ["API_KEY"] = settings.api_key
    response = client.get("/get_commodities", params={"function": "WHEAT", "interval": "monthly"})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["name"] == "Global Price of Wheat"
    assert json_response["interval"] == "monthly"
    assert json_response["unit"] == "dollar per metric ton"
    assert isinstance(json_response["data"], list)
    assert len(json_response["data"]) > 0 
    assert "date" in json_response["data"][0]
    assert "value" in json_response["data"][0]
