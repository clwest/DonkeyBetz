import os
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain.vectorstores.pgvector import PGVector
from services.logging_config import root_logger as logger
from content_loaders.process_urls import ingest_urls
from content_loaders.process_pdfs import ingest_pdfs
from content_loaders.process_youtube import ingest_videos
from langchain_community.chat_message_histories import PostgresChatMessageHistory

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CONNECTION_STRING = os.getenv("DEV_DATABASE_URL")

class LangchainUtility:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small", openai_api_key=self.openai_api_key
        )
        self.llm = ChatOpenAI(
            verbose=True,
            model="gpt-4o",
            temperature=0.3,
            openai_api_key=self.openai_api_key,
        )
        self.memory = ConversationSummaryMemory(
            llm=self.llm,
            memory_key="chat_history",
            k=5,
            return_messages=True,
        )
    
    def generate_embeddings(self, embed_data, collection_name):
        try:
            logger.debug(f"Combined data: {embed_data[:5]}")
            vectorstore = PGVector(
                collection_name=collection_name,
                connection_string=CONNECTION_STRING,
                embedding_function=self.embeddings,
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
    
    def ingest_and_embed_content(self, content_type, content_data, collection_name):
        processed_data = []
        
        if content_type == "url":
            urls, url_title = content_data['urls'], content_data['url_title']
            processed_data = ingest_urls(urls, url_title, collection_name)
        elif content_type == "pdf":
            processed_data = ingest_pdfs(content_data)
        elif content_type == "videos":
            processed_data = ingest_videos(content_data)
        else:
            logger.error(f"Unsupported content type: {content_type}")
            raise ValueError(f"Unsupported content type: {content_type}")

        if processed_data:
            embeddings_count, vectorstore = self.generate_embeddings(
                processed_data, collection_name
            )
            logger.info(f"Processed and stored {embeddings_count} embeddings.")
            return processed_data
        else:
            logger.info("No data processed")
            return processed_data

    def llm_query(self, query, formatted_chat_history, collection_name):
        retriever = PGVector.from_existing_index(
            embedding=self.embeddings,
            collection_name=collection_name,
            connection_string=CONNECTION_STRING,
        )

        qa_retriever = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever.as_retriever(),
            memory=self.memory,
        )

        response = qa_retriever(
            {"question": query, "chat_history": formatted_chat_history}
        )
        return response
    
    def get_chat_history(self, session_id):
        chat_history = PostgresChatMessageHistory(
            session_id=str(session_id),
            connection_string=CONNECTION_STRING,
        )
        return chat_history

    @staticmethod
    def format_past_conversations(past_conversations):
        formatted_conversations = []
        for conversation in past_conversations:
            message_type = conversation.type
            if message_type not in ["user", "ai", "system", "human"]:
                raise ValueError(f"Unknown message type: {message_type}")

            formatted_conversations.append(
                {"type": message_type, "content": conversation.content}
            )

        return formatted_conversations