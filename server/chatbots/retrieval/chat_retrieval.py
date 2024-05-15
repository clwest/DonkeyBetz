import logging
import os
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain.vectorstores.pgvector import PGVector
from factory.token_factory import TokenCounterFactory
from services.logging_config import root_logger as logger

CONNECTION_STRING = os.getenv("DEV_DATABASE_URL")


class ChatRetrievalLLM:
    def __init__(self):
        load_dotenv()
        self.openai_api = os.getenv("OPENAI_API_KEY")
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small", openai_api_key=self.openai_api
        )

        self.llm = ChatOpenAI(
            verbose=True,
            model="gpt-4-1106-preview",
            temperature=0.3,
            openai_api_key=self.openai_api,
        )

        self.memory = ConversationSummaryMemory(
            llm=self.llm,
            memory_key="chat_history",
            k=5,
            return_messages=True,
        )

    def llm_query(self, query, formatted_chat_history, collection_name):
        self.retriever = PGVector.from_existing_index(
            embedding=self.embeddings,
            collection_name=collection_name,
            connection_string=os.getenv("DEV_DATABASE_URL"),
        )

        self.qa_retriever = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever.as_retriever(),
            memory=self.memory,
        )

        response = self.qa_retriever(
            {"question": query, "chat_history": formatted_chat_history}
        )
        return response

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
