import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("CRYPTONEWS")
api = os.getenv("CRYPTO_NEWS_API")


# General Crypto News
def all_ticker_news():
    url = f"{BASE_URL}/category"
    params = {"section": "alltickers", "items": 3, "page": 5, "token": api}
    response = requests.get(url, params=params)
    data = response.json().get("data")
    if not data:
        return
    ticker_list = []
    for ticker in data:
        ticker_dict = {
            "news_url": ticker["news_url"],
            "image_url": ticker["image_url"],
            "title": ticker["title"],
            "text": ticker["text"],
            "source_name": ticker["source_name"],
            "date": ticker["date"],
            "topics": ticker["topics"],
            "sentiment": ticker["sentiment"],
            "type": ticker["type"],
            "tickers": ticker["tickers"],
        }
        ticker_list.append(ticker_dict)
    return ticker_list


def crypto_news(source_name=None):
    url = f"{BASE_URL}/category"
    params = {"section": "general", "items": 5, "page": 5, "token": api}
    if source_name:
        params["source_name"] = source_name
    response = requests.get(url, params=params)
    response_data = response.json().get("data", [])
    if not response_data:
        return []
    news_list = []
    for news in response_data:
        news_dict = {
            "news_url": news["news_url"],
            "image_url": news["image_url"],
            "title": news["title"],
            "text": news["text"],
            "source_name": news["source_name"],
            "date": news["date"],
            "topics": news["topics"],
            "sentiment": news["sentiment"],
            "type": news["type"],
        }
        news_list.append(news_dict)
    return news_list


def trending_headlines(ticker=None):
    url = f"{BASE_URL}/trending-headlines"
    params = {"page": 1, "token": api}
    if ticker:
        params["ticker"] = ticker
    response = requests.get(url, params=params)
    data = response.json().get("data", [])
    if not data:
        return []
    trending_list = []
    for trending in data:
        trending_dict = {
            "id": trending["id"],
            "headline": trending["headline"],
            "text": trending["text"],
            "news_id": trending["news_id"],
            "date": trending["date"],
            "tickers": trending["tickers"],
            "sentiment": trending["sentiment"],
        }
        trending_list.append(trending_dict)
    return trending_list


def get_event_articles(tickers=None):
    event_url = f"{BASE_URL}/events"
    event_params = {"page": 1, "token": api}
    event_response = requests.get(event_url, params=event_params)
    event_data = event_response.json().get("data", [])

    article_url = f"{BASE_URL}/events"
    article_params = {
        "page": 1,
        "token": api,
    }
    event_list = []
    for event in event_data:
        event_id = event["event_id"]
        article_params["eventid"] = event_id
        if tickers:
            article_params["tickers"] = tickers
        article_response = requests.get(article_url, params=article_params)
        article_data = article_response.json().get("data", [])
        articles_for_event = []
        for article in article_data:
            article_dict = {
                "title": article["title"],
                "news_url": article["news_url"],
                "image_url": article["image_url"],
                "text": article["text"],
                "sentiment": article["sentiment"],
                "type": article["type"],
                "source_name": article["source_name"],
                "date": article["date"],
                "tickers": article["tickers"],
                "topics": article["topics"],
            }
            articles_for_event.append(article_dict)
        event_dict = {
            "event_name": event["event_name"],
            "event_text": event["event_text"],
            "event_id": event["event_id"],
            "news_items": event["news_items"],
            "date": event["date"],
            "tickers": event["tickers"],
            "articles": articles_for_event,
        }
        event_list.append(event_dict)
    return event_list


def get_top_mentioned_crypto_tickers():
    url = f"{BASE_URL}/top-mention"
    params = {"date": "last7days", "token": api}
    response = requests.get(url, params=params)
    data = response.json()["data"]["all"]
    if not data:
        return
    mention_list = []
    for mention in data:
        mention_dict = {
            "total_mentions": mention["total_mentions"],
            "positive_mentions": mention["positive_mentions"],
            "negative_mentions": mention["negative_mentions"],
            "neutral_mentions": mention["neutral_mentions"],
            "ticker": mention["ticker"],
            "name": mention["name"],
            "sentiment_score": mention["sentiment_score"],
        }
        mention_list.append(mention_dict)
    return mention_list
