import logging
import os
from pprint import pprint
from dotenv import load_dotenv

from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain.vectorstores import Pinecone
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from factory.pinecone_factory import init_pinecone

load_dotenv()
init_pinecone()
index_name = os.getenv("PINECONE_INDEX")
logging.info(f"Pinecone index name: {index_name}")
openai_api = os.getenv("OPENAI_API")


logging.basicConfig(level=logging.INFO)


def debug_pinecone_retrieval(query, embeddings):
    logging.info("Debugging Pinecone Retrieval")
    try:
        # Initialize Pinecone retriever
        retriever = Pinecone.from_existing_index(
            embedding=embeddings,
            index_name=index_name,
        )

        # Retrieve Pinecone index information
        index_info = retriever.get_pinecone_index(index_name)
        logging.info(f"Pinecone Index Info: {index_info}")

        # Generate embeddings for the query
        # Ensure the query is a string and correctly formatted
        if isinstance(query, str):
            test_query_vector = embeddings.embed_query(query)  # Pass string directly
        else:
            logging.error("Query is not a string.")
            return None

        # Perform a test retrieval
        test_retrieval = retriever.as_retriever(test_query_vector)
        logging.info(f"Test Retrieval Results: {test_retrieval}")

    except Exception as e:
        logging.error(f"Error in Pinecone Retrieval: {str(e)}")
        return None


# Usage in your chat_retrieval_llm function
# ...
