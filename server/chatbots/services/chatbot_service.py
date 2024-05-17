# chatbots/services/chatbot_service.py

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from chatbots.managers.session_manager import ConversationSessionManager
from chatbots.managers.message_manager import ChatMessageManager
from langchain_community.chat_message_histories import PostgresChatMessageHistory
from services.logging_config import root_logger as logger

load_dotenv()

class ChatbotService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.connection_string = os.getenv("DEV_DATABASE_URL")
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,
            openai_api_key=self.openai_api_key,
        )
        self.session_manager = ConversationSessionManager(self.connection_string)
        self.message_manager = ChatMessageManager(self.connection_string)

    def create_new_session(self, user_id, chatbot_id, topic_name, description):
        new_session, chat_history = self.session_manager.create_new_session(
            user_id, chatbot_id, topic_name, description
        )
        return new_session

    def get_session(self, session_id):
        return self.session_manager.get_session(session_id)

    def get_chat_history(self, session_id):
        return self.session_manager.get_chat_history(session_id)

    def handle_message(self, session_id, user_message):
        try:
            session = self.get_session(session_id)
            chat_history = self.get_chat_history(session_id)

            # Generate prompt from user message and chat history
            prompt = self.generate_prompt(user_message, chat_history)

            # Get response from the LLM
            response = self.llm(prompt)

            # Add user and AI messages to the chat history
            self.message_manager.add_message(session_id, user_message, is_user=True)
            self.message_manager.add_message(session_id, response, is_user=False)

            return response
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            raise

    def generate_prompt(self, user_message, chat_history):
        # Define basic PromptTemplate with placeholders for messages
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. You may not need to use tools for every query - the user might just want to chat!"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Use chat history and user message to fill the template
        prompt = prompt_template.fill(
            chat_history=chat_history,
            input=user_message,
            agent_scratchpad=""
        )
        return prompt