import requests
import os
import json
from dotenv import load_dotenv
from flask import jsonify
from routes.categories.models import Category
from routes.blockchain.models import Blockchain
from routes.projects.models import Project
from helpers.custom_exceptions import *
from factory import db


load_dotenv()


class CoinGeckoService:
    BASE_URL = os.getenv("COINGECKO")
    API_KEY = os.getenv("COINGECKO_API")
    HEADERS = {
        "Accepts": "application/json",
        "X-CG-Pro-API-Key": API_KEY,
    }

    def _make_request(self, endpoint, params={}):
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, headers=self.HEADERS, params=params)
            response.raise_for_status()
            return json.loads(response.text)
        except requests.RequestException as e:
            raise CoinGeckoAPIError(f"CoinGecko API request failed: {e}")

    def categorize_and_store_data(self):
        coins_market_data = self._make_request("/coins/markets")
