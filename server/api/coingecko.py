import requests
import os
import json
from dotenv import load_dotenv
from flask import jsonify
from helpers.custom_exceptions import *
import helpers.helper_functions as hf
from pprint import pprint
from factory import db
from models.blockchain import Blockchain
from sqlalchemy.exc import IntegrityError


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
            if response.status_code == 200:
                response.raise_for_status()
                return json.loads(response.text)
            else:
                print(f"Error fetching details for {endpoint}: {response.status_code}")
                return None
        # except requests.RequestException as e:
        #     raise CoinGeckoAPIError(f"CoinGecko API request failed: {e}")
        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"OOps: Something Else: {err}")
        return None  # Return None if there was an exception

    def add_or_update_blockchain(self, coin):
        pprint(f"Processing coin: {coin['id']}")
        if not isinstance(coin, dict):
            pprint(f"Invalid data format for blockchain: {coin}")
            return
        # Check for exsisting Blockchain
        existing_blockchain = Blockchain.query.filter_by(
            coingecko_id=coin["id"]
        ).first()
        if existing_blockchain:
            try:
                # Update existing Blockchain
                existing_blockchain.name = coin["name"]
                existing_blockchain.symbol = coin["symbol"]
                existing_blockchain.image = coin["image"]["small"]
                existing_blockchain.categories = (coin["categories"],)
                existing_blockchain.hashing_algorithm = coin["hashing_algorithm"]
                existing_blockchain.description = coin["description"]["en"]
                existing_blockchain.hompage = coin["links"]["homepage"]
                existing_blockchain.blockchain_site = coin["links"]["blockchain_site"]
                existing_blockchain.twitter_name = coin["links"]["twitter_screen_name"]
                existing_blockchain.chat_url = coin["links"]["chat_url"]
                existing_blockchain.country_origin = coin["country_origin"]
                existing_blockchain.genesis_date = coin["genesis_date"]
                existing_blockchain.block_time_in_minutes = coin[
                    "block_time_in_minutes"
                ]
                existing_blockchain.market_cap_rank = coin["market_cap_rank"]
                existing_blockchain.total_btc_locked = coin["total_value_locked"]["btc"]
                existing_blockchain.total_usd_locked = coin["total_value_locked"]["usd"]
                existing_blockchain.all_time_high = coin["ath"]["usd"]
                existing_blockchain.all_time_high_date = coin["ath_date"]
                existing_blockchain.all_time_low = coin["atl"]["usd"]
                existing_blockchain.all_time_low_date = coin["atl_date"]
                hf.update_db()
            except IntegrityError as e:
                print(
                    f"Failed to update existing Blockchain: {existing_blockchain.name}"
                )
                print(f"IntegrityError: {e}")
                db.session.rollback()
        else:
            # Add new Blockchain
            new_blockchain = Blockchain(
                name=coin["name"],
                collection_name=coin["name"] + "_network",  # PGVector Collection Name
                symbol=coin["symbol"],
                image=coin["image"]["small"],
                categories=coin["categories"],
                hashing_algorithm=coin["hashing_algorithm"],
                description=coin["description"]["en"],
                homepage=coin["links"]["homepage"],
                blockchain_site=coin["links"]["blockchain_site"],
                chat_url=coin["links"]["chat_url"],
                twitter_name=coin["links"]["twitter_screen_name"],
                country_origin=coin["country_origin"],
                genesis_date=coin["genesis_date"],
                block_time_in_minutes=coin["block_time_in_minutes"],
                market_cap_rank=coin["market_cap_rank"],
                total_btc_locked=coin["total_value_locked"]["btc"],
                total_usd_locked=coin["total_value_locked"]["usd"],
                all_time_high=coin["ath"]["usd"],
                all_time_high_date=coin["ath_date"],
                all_time_low=coin["atl"]["usd"],
                all_time_low_date=coin["atl_date"],
            )
            hf.add_to_db(new_blockchain)

    def get_coins_market(self):
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": False,
        }
        response = self._make_request("/coins/markets", params)
        market_list = [
            {
                "name": market["id"],
                "symbol": market["symbol"],
                "image": market["image"],
                "price": market["current_price"],
                "market cap": market["market_cap"],
                "market cap rank": market["market_cap_rank"],
                "24 hour percentage change": market["price_change_percentage_24h"],
            }
            for market in response
        ]
        return jsonify(market_list), 200

    def get_top_25_ticker(self):
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 25,
            "page": 1,
            "sparkline": False,
        }
        response_data = self._make_request("/coins/markets", params)
        token_list = [
            {
                "symbol": token["symbol"],
                "image": token["image"],
                "price": token["current_price"],
                "24 hour percentage change": token["price_change_percentage_24h"],
            }
            for token in response_data
        ]
        return jsonify(token_list), 200
