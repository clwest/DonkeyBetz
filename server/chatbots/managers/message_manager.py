import os
import uuid
from factory import db 
from models.chatbots import ChatMessage, ConversationSession
import helpers.helper_functions as hf
import helpers.custom_exceptions as ce
from services.logging_config import root_logger as logger



    # Rest of the code...
class ChatMessageManger:
    def __init__(self, db_session):
        self.db_session = db_session


    def create_message(self, session_id, sender_id, message_type, content):
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
        try:
            message = hf.get_db_object(ChatMessage, message_id)
            return message
        except Exception as e:
            logger.error(f"Error getting message: {e}")
            raise ce.BadRequestError()

    def get_all_messages(self, session_id, sender_id=None):
        try:
            messages = hf.get_db_objects(ChatMessage, session_id=session_id)
            if sender_id:
                query = query.filter_by(sender_id=sender_id)
            messages = query.all()
            return messages
        except Exception as e:
            logger.error(f"Error getting all messages: {e}")
            raise cd.BadRequestError()

    def get_messages_for_session(self, session_id):
        try:
            messages = hf.get_db_objects(ChatMessage, session_id=session_id)
        except Exception as e:
            logger.error(f"Error getting messages for session: {e}")
            raise ce.BadRequestError()
        
        return messages

    def update_message(self, message_id, content):
        try:
            message = hf.get_db_object(ChatMessage, message_id=message_id, content=content)
            if message:
                message.content = content
                hf.update_db()
            else:
                raise ValueError("Message not found")
        except Exception as e:
            logger.error(f"Error updating message: {e}")
            raise ce.BadRequestError()


    def delete_message(self, message_id):
        try:
            message = hf.get_db_object(ChatMessage, message_id)
            hf.delete_from_db(message)
        except Exception as e:
            logger.error(f"Error deleting message: {e}")
            raise ce.BadRequestError()
        