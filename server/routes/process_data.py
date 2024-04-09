import re
import logging
import uuid
import os
from pprint import pprint
from datetime import datetime, timedelta
from dotenv import load_dotenv
import spacy
import asyncio

# Flask configuration
from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request, jsonify, make_response, current_app
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from content_loaders.process_urls import ingest_urls
from content_loaders.process_pdfs import ingest_pdfs
from content_loaders.process_youtube import ingest_videos
from chatbots.embeddings.generate_embeddings import generate_embeddings
from models.users import Project, DocumentType
from services.logging_config import root_logger as logger
import helpers.custom_exceptions as ce
import helpers.helper_functions as hf

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CONNECTION_STRING = os.getenv("DEV_DATABASE_URL")



process_data_blp = Blueprint("/process-data", "process-data", url_prefix="/api/process-data")   

@process_data_blp.route("/url", methods=["POST"])
def process_url():
    data = request.get_json()
    url = data.get("url")
    title = data.get("url_title", "Default Title")
    collection_name = data.get("collection_name", "Default Collection")
    content_type = 'url'

    if not url:
        return jsonify({'error': "URL is required"}), 400
    
    return process_content(url, content_type, title, collection_name)

@process_data_blp.route("/pdf", methods=["POST"])
def process_pdf():
    data = request.get_json()
    pdf_link = data.get("pdf")
    title = data.get("pdf_title", "Default PDF Title")
    collection_name = data.get("collection_name", "Default Collection")
    content_type = 'pdf'

    if not pdf_link:
        return jsonify({'error': "PDF link is required"}), 400

    return process_content(pdf_link, content_type, title, collection_name)

@process_data_blp.route("/video", methods=["POST"])
def process_video():
    data = request.get_json()
    video_link = data.get('video')
    title = data.get('video_title', "Default Video Title")
    collection_name = data.get("collection_name", "Default Collection")
    content_type = 'video'

    if not video_link:
        return jsonify({'error': "Video link is required"}), 400

    return process_content(video_link, content_type, title, collection_name)



def process_content(content, content_type, title, collection_name):
    process_functions = {
        'url': ingest_urls,
        'pdf': ingest_pdfs,
        'video': ingest_videos
    }
    process_func = process_functions.get(content_type)

    if not process_func:
        logger.error(f"Invalid content type: {content_type}")
        return jsonify({"error": "Invalid content type"}), 400

    try:
        processed_content = process_func(content, title, collection_name)
        processed_text = ' '.join([doc.page_content for doc in processed_content])
        processed_count = generate_embeddings(processed_content, OPENAI_API_KEY, CONNECTION_STRING, collection_name)
        logger.info(f"Generated embeddings for {processed_count} items of type {content_type}")

        existing_project = Project.query.filter_by(collection_name=collection_name).first()
        if not existing_project:
            for item in processed_content:
                new_project = Project(
                    title = item.metadata.get("title", "No title"),
                    collection_name=collection_name,
                    source_type=getattr(DocumentType, content_type.upper()),
                    content = processed_text
                )
                hf.add_to_db(new_project)
                logger.info(f"New project added to database with title: {new_project.title}")
                return jsonify({"message": f"New project created with {processed_count} items processed"}), 201
        else:
            logger.warning(f"Project with collection name {collection_name} already exists")
            return jsonify({"warning": "Project already exists"}), 409
    
    except Exception as e:
        logger.error(f"Error processing {content_type}: {e}")
        return jsonify({"error": "Failed to process {content_type} due to {str(e)}"}), 500

