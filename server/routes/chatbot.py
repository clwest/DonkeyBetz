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
from schemas.chatbots import ChatbotSchema
from models.users import User, UserQuery
from utils.content_utils import *
from services.logging_config import root_logger as logger
import helpers.custom_exceptions as ce
import helpers.helper_functions as hf
from chatbots.managers.chatbot_manager import ChatbotManager
from chatbots.managers.message_manager import ChatMessageManger
from chatbots.managers.session_manager import ConversationSessionManager


load_dotenv()

# Function to register a new Chatbot
chatbot_blp = Blueprint("chatbot", "chatbot", url_prefix="/api/chatbot")
chatbot_schema = ChatbotSchema()
# chatbot_manager = ChatbotManager()


@chatbot_blp.route('/chatbot', methods=['POST'])
def create_chatbot():
    # Deserialize and validate the incoming JSON data
    try:
        chatbot_data = chatbot_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    # Initialize ChatbotManager with the current database session
    chatbot_manager = ChatbotManager(db.session)

    # Use the ChatbotManager to create a new Chatbot
    try:
        chatbot = chatbot_manager.create_chatbot(**chatbot_data)
        # Serialize the new chatbot instance for the response
        return chatbot_schema.dump(chatbot), 201
    except Exception as e:
        logger.error(f"Failed to create chatbot: {e}")
        return jsonify({"error": "Failed to create chatbot"}), 500

    # # Serialize the new chatbot instance for the response
    # return schema.dump(chatbot), 201

@chatbot_blp.route("/process-urls", methods=["POST"])
def process_urls():
    data = request.json
    urls = data.get('urls')
    if urls:
        chatbot_manager.process_url_links(urls)
        return jsonify({"message": "Content processed"}), 200
    else:
        return jsonify({"error": "No URLs provided"}), 400


# @chatbot_blp.route("/blockchain-docs", methods=["POST"])
# @jwt_required()
# def handle_chat_interaction():
#     # from factory import db
#     from chatbots.retrieval.chat_retrieval import ChatRetrievalLLM
#     from chatbots.prompts.chat_manager import ChatManager
#     from chatbots.memory.message_history import MessageHistoryManager

#     try:
#         user_id = get_jwt_identity()["id"]
#         user = User.query.get(user_id)
#         user_email = user.email
#         data = request.get_json()
#         query = data.get("query", "")
#         topic_name = generate_topic_name(query, nlp)
#         entities = extract_entities(query, nlp)
#         session_id = get_or_create_conversation_session(user_id, query, "")
#         connection_string = os.getenv("DEV_DATABASE_URL")
#         collection_name = "fuel_network"

#         # Initialize components
#         chat_manager = ChatManager()
#         chat_retrieval_system = ChatRetrievalLLM()
#         custom_message_converter = CustomMessageConverter(author_email=user_email)
#         message_history_manager = MessageHistoryManager(
#             session_id, connection_string, custom_message_converter
#         )

#         # Process query and generate response
#         selected_prompt = chat_manager.run_query(query)
#         combined_chat_history = message_history_manager.get_formatted_conversations()
#         final_response = chat_retrieval_system.llm_query(
#             selected_prompt, combined_chat_history, collection_name
#         )

#         # Generate a description of hte AI's response
#         ai_response_description = generate_description(final_response.get("answer", ""))
#         # updated_conversation = update_conversation_session(
#         #     session_id, topic_name, ai_response_description
#         # )

#         # Store and manage history
#         message_history_manager.add_user_message(query)
#         message_history_manager.add_ai_message(final_response)

#         response_data = {
#             "question": query,
#             "answer": final_response["answer"]
#             if isinstance(final_response, dict)
#             else final_response,
#             "topic_name": topic_name,
#             "entities": entities,
#             "summary": ai_response_description,
#             # "update": updated_conversation
#             # "session_description": updated_session.description,
#         }
#         return response_data

#     except Exception as e:
#         logger.error(f"Error in chat retrieval: {str(e)}")
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500