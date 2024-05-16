import os
import uuid
from datetime import datetime, timedelta
from langchain_community.chat_message_histories import PostgresChatMessageHistory
from dotenv import load_dotenv

from models.chatbots import ConversationSession
import helpers.helper_functions as hf
import helpers.custom_exceptions as ce
from services.logging_config import root_logger as logger

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")




class ConversationSessionManager:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        
    def create_new_session(self, user_id, chatbot_id, topic_name, description, session_metadata=None):
        try:
            new_session = ConversationSession(
                id = str(uuid.uuid4()),
                user_id=user_id,
                chatbot_id=chatbot_id,
                topic_name=topic_name,
                description=description,
                conversation_status="ACTIVE",
                session_metadata=session_metadata
            )
            hf.add_to_db(new_session)
            
            chat_history = PostgresChatMessageHistory(
                session_id=str(new_session.id),
                connection_string=self.connection_string,
            )
            return new_session, chat_history
        except Exception as e:
            logger.error(f"Error creating a new session for user {user_id} with chatbot {chatbot_id}: {e}")
            raise ce.BadRequestError()
        
    def get_session(self, session_id):
        try:
            session = hf.get_db_object(ConversationSession, id=session_id)
            return session
        except Exception as e:
            logger.error(f"Error getting session {session_id}: {e}")
            
    def get_all_sessions(self, user_id, chatbot_id):
        try:
            sessions = hf.get_db_objects(ConversationSession, user_id=user_id, chatbot_id=chatbot_id)
            return sessions
        except Exception as e:
            logger.error(f"Error getting all sessions for user {user_id} and chatbot {chatbot_id}: {e}")
            raise ce.BadRequestError()
        
    def update_sessions_status(self, session_id, new_status):
        try:
            session = hf.get_db_object(ConversationSession, id=session_id)
            if session:
                session.conversation_status = new_status
                hf.update_db()
                return session
            else:
                raise ce.ResourceNotFoundError(f"Session with ID {session_id} not found")
        except Exception as e:
            logger.error(f"Error updating session {session_id} status to {new_status}": {e})
            raise ce.BadRequestError()
    
    def get_sessions_by_status(self, user_id, chatbot_id, status):
        try:
            sessions = hf.get_db_objects(ConversationSession, user_id=user_id, chatbot_id=chatbot_id, conversation_status=status)
            return sessions
        except Exception as e:
            logger.error(f"Error getting {status} sessions for user {user_id} and chatbot {chatbot_id}: {e}")
            raise ce.BadRequestError()
        
    def pause_session(self, session_id):
        try:
            session = self.update_session_status(session_id, "PAUSED")
            return session
        except Exception as e:
            logger.error(f"Error pausing session {session_id}: {e}")
            raise ce.BadRequestError()
    
    def archive_session(self, session_id):
        try:
            session = self.update_sessions_status(session_id, "ARCHIVED")
            return session
        except Exception as e:
            logger.error(f"Error archiving session {session_id}: {e}")
            raise ce.BadRequestError()
    
    def resume_session(self, session_id):
        try:
            session = self.update_sessions_status(session_id, "ACTIVE")
            return session
        except Exception as e:
            logger.error(f"Error resuming session {session_id}: {e}")
            raise ce.BadRequestError()
    
    def end_session(self, session_id):
        try:
            session = self.update_sessions_status(session_id, "ARCHIVED")
            return session
        except Exception as e:
            logger.error(f"Error ending session {session_id}: {e}")
            raise ce.BadRequestError()
    
    def delete_session(self, session_id):
        try:
            session = hf.get_db_object(ConversationSession, id=session_id)
            if session:
                hf.delete_from_db(session)
            else:
                raise ce.ResourceNotFoundError(f"Session with ID {session_id} not found")
        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {e}")
            raise ce.BadRequestError()
    
    def add_message(self, session_id, message_content, is_user):
        try:
            chat_history = PostgresChatMessageHistory(
                session_id=str(session_id),
                connection_string=self.connection_string,
            )
            if is_user:
                chat_history.add_user_message(message_content)
            else:
                chat_history.add_ai_message(message_content)
        except Exception as e:
            logger.error(f"Error adding message to session {session_id}: {e}")
            raise ce.BadRequestError()
    
    def get_messages(self, session_id):
        try:
            chat_history = PostgresChatMessageHistory(
                session_id=str(session_id),
                connection_string=self.connection_string,
            )
            messages = chat_history.get_messages()
            return messages
        except Exception as e:
            logger.error(f"Error getting messages for session {session_id}: {e}")
            raise ce.BadRequestError()
        
    def get_chat_history(self, session_id):
        try:
            chat_history = PostgresChatMessageHistory(
                session_id=str(session_id),
                connection_string=self.connection_string,
            )
            return chat_history
        except Exception as e:
            logger.error(f"Error getting chat history for session {session_id}: {e}")
            raise ce.BadRequestError()
        
    def check_session_duration(self, session_id, max_duration=3600):
        try:
            session = self.get_session(session_id)
            duration = (datetime.now() - session.created_at).total_seconds()
            return duration <= max_duration
        except Exception as e:
            logger.error(f"Error checking session duration for session {session_id}: {e}")
            raise ce.BadRequestError()
        
    def check_token_limit(self, session_id, max_tokens=3000):
        try:
            chat_history = self.get_chat_history(session_id)
            token_count = sum(len(message["content"]) for message in chat_history.get_messages())
            return token_count <= max_tokens
        except Exception as e:
            logger.error(f"Error checking token limit for session {session_id}: {e}")
            raise ce.BadRequestError()