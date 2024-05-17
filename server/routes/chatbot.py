import os
import re
import uuid
import logging
import spacy
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pprint import pprint
from flask import request, jsonify, make_response
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required
from flask_smorest import Blueprint
from marshmallow import ValidationError

from factory import db
from models.users import User, UserQuery
from chatbots.services.chatbot_service import ChatbotService
from schemas.chatbots import ChatbotSchema, ConversationSessionSchema
from chatbots.managers.chatbot_manager import ChatbotManager
from chatbots.managers.message_manager import ChatMessageManager
from chatbots.managers.session_manager import ConversationSessionManager
from chatbots.utils.langchain_utility import LangchainUtility
import helpers.custom_exceptions as ce
import helpers.helper_functions as hf
from services.logging_config import root_logger as logger

load_dotenv()

# Function to register a new Chatbot
chatbot_blp = Blueprint("chatbot", "chatbot", url_prefix="/api/chatbot")
chatbot_service = ChatbotService()
chatbot_schema = ChatbotSchema()
session_schema = ConversationSessionSchema()

@chatbot_blp.route('/chatbot', methods=['POST'])
def create_chatbot():
    # Deserialize and validate the incoming JSON data
    try:
        chatbot_data = chatbot_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    # Use the ChatbotManager to create a new Chatbot
    try:
        chatbot = chatbot_service.create_chatbot(**chatbot_data)
        # Serialize the new chatbot instance for the response
        return chatbot_schema.dump(chatbot), 201
    except Exception as e:
        logger.error(f"Failed to create chatbot: {e}")
        return jsonify({"error": "Failed to create chatbot"}), 500

@chatbot_blp.route("/chat", methods=["POST"])
@jwt_required()
def handle_chat_interaction():
    try:
        user_id = get_jwt_identity()["id"]
        data = request.get_json()
        session_id = data.get("session_id")
        user_message = data.get("message")
        
        if not session_id or not user_message:
            return jsonify({"error": "session_id and message are required"}), 400
        
        response = chatbot_service.handle_message(session_id, user_message)
        return jsonify({"response": response}), 200
    except Exception as e:
        logger.error(f"Error in chat interaction: {e}")
        return jsonify({"error": str(e)}), 500
    
@chatbot_blp.route("/session", methods=["POST"])
@jwt_required()
def create_sessionO():
    try:
        user_id = get_jwt_identity()["id"]
        data = request.json()
        chatbot_id = data.get("chatbot_id")
        topic_name = data.get("topic_name")
        description = data.get("description")
        
        if not chatbot_id or not topic_name or not description:
            return jsonify({"error": "chatbot_id, topic_name, and description are required"}), 400
        
        new_session = chatbot_service.create_new_session(user_id, chatbot_id, topic_name, description)
        return session_schema.dump(new_session), 201
    except Exception as e:
        logger.error(f"Error create session: {e}")
        return jsonify({"error": str(e)}), 500

@chatbot_blp.route("/process-urls", methods=["POST"])
def process_urls():
    data = request.json
    urls = data.get('urls')
    collection_name = data.get('collection_name', 'default_collection')
    if urls:
        langchain_utility = LangchainUtility()
        processed_content = langchain_utility.ingest_and_embed_content("url", urls, collection_name)
        return jsonify({"message": "Content processed", "processed_content": processed_content}), 200
    else:
        return jsonify({"error": "No URLs provided"}), 400

@chatbot_blp.route("/process-pdfs", methods=["POST"])
def process_pdfs():
    data = request.json
    pdfs = data.get('pdfs')
    collection_name = data.get('collection_name', 'default_collection')
    if pdfs:
        langchain_utility = LangchainUtility()
        processed_content = langchain_utility.ingest_and_embed_content("pdf", pdfs, collection_name)
        return jsonify({"message": "Content processed", "processed_content": processed_content}), 200
    else:
        return jsonify({"error": "No PDFs provided"}), 400

@chatbot_blp.route("/process-videos", methods=["POST"])
def process_videos():
    data = request.json
    videos = data.get('videos')
    collection_name = data.get('collection_name', 'default_collection')
    if videos:
        langchain_utility = LangchainUtility()
        processed_content = langchain_utility.ingest_and_embed_content("videos", videos, collection_name)
        return jsonify({"message": "Content processed", "processed_content": processed_content}), 200
    else:
        return jsonify({"error": "No videos provided"}), 400

