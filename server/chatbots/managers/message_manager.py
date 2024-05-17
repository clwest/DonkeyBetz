import os
import uuid
from factory import db
from models.chatbots import ChatMessage, ConversationSession
import helpers.helper_functions as hf
import helpers.custom_exceptions as ce
from services.logging_config import root_logger as logger


class ChatMessageManager:
    """
    Manager class for handling chat messages.
    
    Attributes:
        db_session: the database session
        
    Methods:
        create_message: Creates a new chat message.
        get_message: Retrieves a chat message by its ID.
        get_all_messages: Retrieves all messages for a session and for optionally for a sender.
        get_messages_for_session: Retrieves messages for a specific session.
        update_message: Updates the content of a chat message.
        delete_message: Deletes a chat message.
    """
    def __init__(self, db_session):
        self.db_session = db_session
    
    def create_message(self, session_id, sender_id, message_type, content):
        """
        Creates a new chat message.
        
        Args:
            session_id (str): The ID of the conversation session.
            sender_id (str): The ID of the sender.
            message_type (str): The type of message (e.g., 'user', 'ai').
            content (str): The content of the message.
        
        Returns:
            ChatMessage: The created chat message.
            
        Raises:
            ValueError: If the session is not found.
        """
        session = self.db_session.query(ConversationSession).filter_by(id=session_id).first()
        
        if not session:
            raise ValueError(f"Session not found")
        
        new_message = ChatMessage(
            session_id=session_id,
            sender_id=sender_id,
            message_type=message_type,
            content=content
        )
        hf.add_to_db(new_message)
        return new_message
    
    def get_message(self, message_id):
        """
        Retrieves a chat message by its ID.
        
        Args:
            message_id (int): The ID of the chat message.
            
        Returns:
            ChatMessage: The retrieved chat message.
        
        Raises:
            ce.BadRequestError: The there is an error retrieving the message
        """
        try:
            message = hf.get_db_object(ChatMessage, id=message_id)
            return message
        except Exception as e:
            logger.error(f"Error getting message: {e}")
            raise ce.BadRequestError()
    
    def get_all_messages(self, session_id, sender_id=None):
        """
        Retrieves all messages for a session and optionally for a sender.
        
        Args:
            session_id (str): The ID of the conversation session.
            sender_id (str, optional): The ID of the sender
        
        Returns:
            list: A list of chat messages.
        
        Raises:
            ce.BadRequestError: If there is an error retrieving the messages.
        """
        try:
            query = hf.get_db_objects(ChatMessage, session_id=session_id)
            if sender_id:
                query = query.filter_by(sender_id=sender_id)
            messages = query.all()
            return messages
        except Exception as e:
            logger.error(f"Error getting all messages: {e}")
            raise ce.BadRequestError()
        
    def get_messages_for_session(self, session_id):
        """
        Retrieves messages for specific session.
        
        Args:
            session_id (str): The ID of the conversation session.
        
        Returns:
            list: A list of chat messages.
        
        Raises:
            ce.BadRequestError: If there is an error retrieving the messages.
        """
        try:
            messages = hf.get_db_objects(ChatMessage, session_id=session_id)
            return messages
        except Exception as e:
            logger.error(f"Error getting messages for session: {e}")
            raise ce.BadRequestError()
        
    def update_message(self, message_id, content):
        """
        Updates the content of a chat message.
        
        Args:
            message_id (int): The ID of the chat message.
            content (str): The new content for the message.
        
        Raises:
            ce.BadRequestError: If there is an error updating the message.
            ValueError: If the message is not found.
        """
        try:
            message = hf.get_db_object(ChatMessage, id=message_id)
            if message:
                message.content = content
                hf.update_db()
            else:
                raise ValueError("Message not found")
        except Exception as e:
            logger.error(f"error updating message: {e}")
            raise ce.BadRequestError()
        
    def delete_message(self, message_id, content):
        """
        Deletes a chat message.
        
        Args:
            message_id (int): The ID of the chat message.
        
        Raises:
            ce.BadRequestError: If there is an error deleting the message.
        """
        try:
            message = hf.get_db_object(ChatMessage, id=message_id)
            hf.delete_from_db(message)
        except Exception as e:
            logger.error(f"Error deleting message: {e}")
            raise ce.BadRequestError()