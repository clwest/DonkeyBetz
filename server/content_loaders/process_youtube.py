import os
import requests
import spacy
import time  # Import the time module
from pprint import pprint
from dotenv import load_dotenv
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from metadata.transformers import *
from services.logging_config import root_logger as logger


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
nlp = spacy.load("en_core_web_sm")

# Define the rate limit parameters
MAX_REQUESTS_PER_SECOND = 5  # Maximum requests per second
MIN_REQUEST_INTERVAL = 1 / MAX_REQUESTS_PER_SECOND  # Minimum time between requests


class Document:
    def __init__(self, content, metadata=None, lemmatized_text=None):
        self.page_content = content
        self.metadata = metadata or {"title": ""}
        self.lemmatized_text = lemmatized_text or content

    @property
    def title(self):
        return self.metadata.get("title", "No Title")


def ingest_videos(batch_videos, video_title, collection_name):
    """Process and ingest YouTube videos"""
    processed_videos = []
    api_key = os.getenv("YOUTUBE_API_KEY")

    for url in batch_videos:
        try:
            loader = YoutubeLoader.from_youtube_url(
                url,
                add_video_info=True,
            )
            video = loader.load_and_split()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )
            youtube_list = loader.load_and_split(text_splitter)

            for video in youtube_list:
                processed_video = process_videos(
                    video, nlp, video.metadata, video_title, collection_name
                )
                processed_videos.append(processed_video)
            time.sleep(MIN_REQUEST_INTERVAL)

        except Exception as e:
            pprint(f"Failed to load data for URL {url}: {e}")
            logger.error(f"Failed to load data for URL {url}: {e}")

    return processed_videos


def process_videos(video, nlp, metadata, video_title, collection_name):
    """Process individual video for metadata, content, and embeddings"""
    cleaned_text = clean_text(video.page_content)
    lemmatized_text = lemmatize_text(cleaned_text, nlp)
    title = metadata.get("title", "No Title")
    if title == "No Title":
        title = f"{video_title} Youtube"
    metadata_dict = {
        "title": video_title,
        "collection": collection_name,
        "source_type": "Youtube",
    }

    logger.debug(
        f"Processed Video '{title}' with content length: {len(lemmatized_text)} characters"
    )

    processed_data = Document(content=lemmatized_text, metadata=metadata_dict)
    return processed_data


if __name__ == "__main__":
    ingest_videos()
