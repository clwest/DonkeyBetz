import logging
import os
from pprint import pprint
from dotenv import load_dotenv


from langchain.memory.chat_message_histories import SQLChatMessageHistory
from factory.pinecone_factory import init_pinecone
from services.session import get_or_create_session_id


load_dotenv()
init_pinecone()
index_name = os.getenv("PINECONE_INDEX")
logging.info(f"Pinecone index name: {index_name}")
openai_api = os.getenv("OPENAI_API")


logging.basicConfig(level=logging.INFO)


def debug_chat_message_history(session_id):
    try:
        chat_message_history = SQLChatMessageHistory(
            session_id=session_id,
            connection_string=os.getenv("DEV_DATABASE_URL"),
        )

        # Retrieve and log all messages for the given session
        all_messages = chat_message_history.messages
        for message in all_messages:
            logging.info(f"Message: {message.content}")

        return all_messages
    except Exception as e:
        logging.error(f"Error in Chat Message History: {str(e)}")
        return []


# Usage in your chat_retrieval route:
# ...
# debug_messages = debug_chat_message_history(session_id)
# logging.info(f"Debug Messages: {debug_messages}")
