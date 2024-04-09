import os
from dotenv import load_dotenv
import re
import logging
from datetime import datetime

# Flask configuration
from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required

# Helpers and other functions
from factory.limiter_factory import limiter
from helpers.constants import *
from helpers.helper_permissions import *
import helpers.custom_exceptions as ce
import helpers.helper_functions as hf
from factory.app_factory import jwt

# api imports
from api.crypto_news import *

load_dotenv()

crypto_news_blp = Blueprint("crypto_news", "crypto_news", url_prefix="/api/crypto-news")

@crypto_news_blp.route("/all_ticker_news", methods=["GET"])
def get_all_ticker_news():
    ticker_list = all_ticker_news()
    if ticker_list is None:
        return jsonify({"error": "No News found"}), 404
    return jsonify(ticker_list), 200

@crypto_news_blp.route("/crypto_news", methods=["GET"])
def crypto_news():
    news_list = get_crypto_news()
    if news_list is None:
        return jsonify({"Error": "No News found"}), 404
    return jsonify(news_list), 200


@crypto_news_blp.route("/trending_headlines", methods=["GET"])
def get_trending_headlines():
    trending = trending_headlines()
    if trending is None:
        return jsonify({"error": "No Trending headlines"})
    return jsonify(trending), 200