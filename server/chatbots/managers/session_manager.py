import os
import uuid
from langchain_community.chat_message_histories import PostgresChatMessageHistory
from dotenv import load_dotenv

from models.chatbots import ConversationSession
import helpers.helper_functions as hf
import helpers.custom_exceptions as ce
from services.logging_config import root_logger as logger

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class ConversationSessionManager:
    """
    Manager class for handling conversation sessions.

    Args:
        connection_string (str): The connection string for the database.

    Attributes:
        connection_string (str): The connection string for the database.

    Methods:
        create_new_session: Creates a new conversation session.
        get_session: Retrieves a conversation session by session ID.
        get_all_sessions: Retrieves all conversation sessions for a user and chatbot.
        update_session_status: Updates the status of a conversation session.
        get_sessions_by_status: Retrieves conversation sessions by status.
        pause_session: Pauses a conversation session.
        archive_session: Archives a conversation session.
        resume_session: Resumes a paused conversation session.
        end_session: Ends a conversation session.
        delete_session: Deletes a conversation session.
        add_message: Adds a message to a conversation session.
        get_messages: Retrieves all messages for a conversation session.
        get_chat_history: Retrieves the chat history for a conversation session.
    """
    def __init__(self, connection_string):
        self.connection_string = connection_string
        
    def create_new_session(self, user_id, chatbot_id, topic_name, description, session_metadata=None):
        """
        Creates a new conversation session.

        Args:
            user_id (str): The ID of the user.
            chatbot_id (str): The ID of the chatbot.
            topic_name (str): The name of the topic.
            description (str): The description of the session.
            session_metadata (dict, optional): Additional metadata for the session.

        Returns:
            tuple: A tuple containing the new session object and the chat history object.
        """
        try:
            new_session = ConversationSession(
                id = uuid.uuid4(),
                user_id=user_id, 
                chatbot_id=chatbot_id, 
                topic_name=topic_name, 
                description=description,
                conversation_status="ACTIVE",
                session_metadata=session_metadata
                ),
                
            hf.add_to_db(new_session)

            chat_history = PostgresChatMessageHistory(
                    session_id=str(new_session.id),
                    connection_string=self.connection_string,
                )
            return new_session, chat_history
        except Exception as e:
            logger.error(f"Error creating a new session: {e}")
            raise ce.BadRequestError()
    
    def get_session(self, session_id):
        """
        Retrieves a conversation session by session ID.

        Args:
            session_id (str): The ID of the session.

        Returns:
            ConversationSession: The conversation session object.
        """
        try:
            session = hf.get_db_object(ConversationSession, session_id)
            return session
        except Exception as e:
            logger.error(f"Error getting session: {e}")
            raise ce.BadRequestError()

    def get_all_sessions(self, user_id, chatbot_id):
        """
        Retrieves all conversation sessions for a user and chatbot.

        Args:
            user_id (str): The ID of the user.
            chatbot_id (str): The ID of the chatbot.

        Returns:
            list: A list of conversation session objects.
        """
        try:
            sessions = hf.get_db_objects(ConversationSession, user_id=user_id, chatbot_id=chatbot_id)
            return sessions
        except Exception as e:
            logger.error(f"Error getting all sessions: {e}")
            raise ce.BadRequestError()
        
    def update_session_status(self, session_id, topic_name, description):
        """
        Updates the status of a conversation session.

        Args:
            session_id (str): The ID of the session.
            topic_name (str): The name of the topic.
            description (str): The description of the session.
        """
        try:
            session = hf.get_db_object(ConversationSession, id=session_id)
            if session:
                session.conversation_status = new_status
                hf.update_db()
        except Exception as e:
            logger.error(f"Error updating session: {e}")
            raise ce.BadRequestError(f"Session with ID {session.id} not found")

    
    def get_sessions_by_status(self, user_id, chatbot_id, status):
        """
        Retrieves conversation sessions by status.

        Args:
            user_id (str): The ID of the user.
            chatbot_id (str): The ID of the chatbot.
            status (str): The status of the sessions to retrieve.

        Returns:
            list: A list of conversation session objects.
        """
        try:
            sessions = hf.get_db_objects(ConversationSession, user_id=user_id, chatbot_id=chatbot_id, conversation_status=status)
            return sessions
        except Exception as e:
            logger.error(f"Error getting {status} sessions: {e}")
            raise ce.BadRequestError()

    def pause_session(self, session_id):
        """
        Pauses a conversation session.

        Args:
            session_id (str): The ID of the session.
        """
        try:
            session = hf.get_db_object(ConversationSession, session_id)
            session.conversation_status = "PAUSED"
            hf.update_db()
        except Exception as e:
            logger.error(f"Error pausing session: {e}")
            raise ce.BadRequestError()
        
    def archive_session(self, session_id):
        """
        Archives a conversation session.

        Args:
            session_id (str): The ID of the session.
        """
        try:
            session = hf.get_db_object(ConversationSession, session_id)
            session.conversation_status = "ARCHIVED"
            hf.update_db()
        except Exception as e:
            logger.error(f"Error archiving session: {e}")
            raise ce.BadRequestError()

    def resume_session(self, session_id):
        """
        Resumes a paused conversation session.

        Args:
            session_id (str): The ID of the session.
        """
        try:
            session = hf.get_db_object(ConversationSession, session_id)
            session.conversation_status = "ACTIVE"
            hf.update_db()
        except Exception as e:
            logger.error(f"Error resuming session: {e}")
            raise ce.BadRequestError()
        
    def end_session(self, session_id):
        """
        Ends a conversation session.

        Args:
            session_id (str): The ID of the session.
        """
        try:
            session = hf.get_db_object(ConversationSession, session_id)
            session.conversation_status = "ARCHIVED"
            hf.update_db()
        except Exception as e:
            logger.error(f"Error ending session: {e}")
            raise ce.BadRequestError()

    def delete_session(self, session_id):
        """
        Deletes a conversation session.

        Args:
            session_id (str): The ID of the session.
        """
        try:
            session = hf.get_db_object(ConversationSession, session_id)
            hf.delete_from_db(session)
        except Exception as e:
            logger.error(f"Error deleting session: {e}")
            raise ce.BadRequestError() 

    def add_message(self, session_id, message_content, is_user):
        """
        Adds a message to a conversation session.

        Args:
            session_id (str): The ID of the session.
            message_content (str): The content of the message.
            is_user (bool): Indicates whether the message is from the user or AI.
        """
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
            logger.error(f"Error adding message: {e}")
            raise ce.BadRequestError()

    def get_messages(self, session_id):
        """
        Retrieves all messages for a conversation session.

        Args:
            session_id (str): The ID of the session.

        Returns:
            list: A list of message objects.
        """
        try:
            chat_history = PostgresChatMessageHistory(
                session_id=str(session_id),
                connection_string=self.connection_string,
            )
            messages = chat_history.get_messages()
            return messages
        except Exception as e:
            logger.error(f"Error getting messages: {e}")
            raise ce.BadRequestError()
        
    def get_chat_history(self, session_id):
        """
        Retrieves the chat history for a conversation session.

        Args:
            session_id (str): The ID of the session.

        Returns:
            PostgresChatMessageHistory: The chat history object.
        """
        try:
            chat_history = PostgresChatMessageHistory(
                session_id=str(session_id),
                connection_string=self.connection_string,
            )
            return chat_history
        except Exception as e:
            logger.error(f"Error getting chat history: {e}")
            raise ce.BadRequestError()