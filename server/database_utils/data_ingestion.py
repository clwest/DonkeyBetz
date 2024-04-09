from pprint import pprint
import os
from dotenv import load_dotenv


from backend.services.logging_config import configure_logging
from metadata.transformers import *
import helpers.custom_exceptions as ce
import helpers.helper_functions as hf
from factory.pinecone_factory import init_pinecone
from models.blockchain import BlockchainDocument
from models.poker import PokerDocument
from factory import create_app


load_dotenv()
init_pinecone()
openai_key = os.getenv("OPENAI_API")
app = create_app()
configure_logging(app)


def insert_into_postgres(data, data_type):
    try:
        for item in data:
            if isinstance(item, dict) and isinstance(item.get("metadata", {}), dict):
                document = None
                if data_type == "blockchain":
                    document = BlockchainDocument(
                        title=item.get("metadata", {}).get("title", "No Title"),
                        content=item.get("page_content"),
                        source_url=item.get("source_url", ""),
                        source_type=item.get("source_type", ""),
                        blockchain_metadata=item.get("blockchain_metadata", {}),
                        blockchain_name=item.get("blockchain_name", ""),
                    )
                    print(f"Document added to Postgres database: {document}")
                    hf.add_to_db(document)
                elif data_type == "poker":
                    document = PokerDocument(
                        title=item.get("metadata", {}).get("title", "No Title"),
                        content=item.get("page_content"),
                        source_url=item.get("source_url", ""),
                        source_type=item.get("source_type", ""),
                        player_metadata=item.get("player_metadata", {}),
                        player_name=item.get("player_name", ""),
                    )
                    hf.add_to_db(document)
        else:
            app.logger.error(f"Unexpected data format: {item}")

    except Exception as e:
        app.logger.error(f"Error inserting document into database: {e}")
