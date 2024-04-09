import os
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
import helpers.custom_exceptions as ce
from services.logging_config import root_logger as logger

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CONNECTION_STRING = os.getenv("DEV_DATABASE_URL")


def generate_embeddings(embed_data, OPENAI_API_KEY, connection_string, collection_name):
    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY
        )

        logger.debug(f"Combined data: {embed_data[:5]}")
        vectorstore = PGVector(
            collection_name=collection_name,
            connection_string=connection_string,
            embedding_function=embeddings,
        )
        logger.debug("Embedding generation completed")
        logger.info(
            f"Generated {len(embed_data)} embeddings to insert into PGVector: {collection_name}"
        )

        vectorstore.add_documents(embed_data)
        logger.info(f"Embeddings added to the database")

        return len(embed_data), vectorstore

    except Exception as e:
        logger.error(f"Error generating embeddings or adding to the database: {e}")
        return 0


if __name__ == "__main__":
    generate_embeddings()
