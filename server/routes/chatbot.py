import re
import logging
import uuid
import os
from pprint import pprint
from datetime import datetime, timedelta
from dotenv import load_dotenv
import spacy

# Flask configuration
from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

# Langchain
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# Helpers, Managers and other functions
from factory.limiter_factory import limiter
from factory import db
from utils.content_utils import *
from chatbots.services.chat_retrieval import ChatRetrievalService
from models.users import User
from models.chatbots import Chatbot, ConversationSession, ChatMessage
import helpers.helper_functions as hf
import helpers.custom_exceptions as ce
from services.logging_config import root_logger as logger

load_dotenv()
chatbot_blp = Blueprint("chatbot", "chatbot", url_prefix="/api/chatbot")

@chatbot_blp.route("/query", methods=["POST"])
@jwt_required()
def handle_query():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        data = request.get_json()
        query = data.get("query", "")
        collection_name = data.get("collection_name", "default_collection")

        chat_retrieval_service = ChatRetrievalService()
        formatted_history = chat_retrieval_service.format_past_conversations(user.chat_messages)
        response = chat_retrieval_service.query_llm(query, formatted_history, collection_name)

        # Save the user query and AI response
        session_id = str(uuid.uuid4())
        user_query = ChatMessage(session_id=session_id, sender_id=user_id, message_type="user", content=query)
        ai_response = ChatMessage(session_id=session_id, sender_id="AI", message_type="ai", content=response["answer"])
        hf.add_to_db(user_query)
        hf.add_to_db(ai_response)

        return jsonify(response)
    except Exception as e:
        logger.error(f"Error handling query: {e}")
        return jsonify({"error": str(e)}), 500



