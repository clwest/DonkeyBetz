
import logging
import os
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain.vectorstores.pgvector import PGVector

load_dotenv()

class ChatRetrievalService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.connection_string = os.getenv("DEV_DATABASE_URL")
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=self.openai_api_key)
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.3, openai_api_key=self.openai_api_key)
        self.memory = ConversationSummaryMemory(llm=self.llm, memory_key="chat_history", k=5, return_messages=True)

    def query_llm(self, query, chat_history, collection_name):
        retriever = PGVector.from_existing_index(embedding=self.embeddings, collection_name=collection_name, connection_string=self.connection_string)
        qa_retriever = ConversationalRetrievalChain.from_llm(llm=self.llm, retriever=retriever.as_retriever(), memory=self.memory)
        response = qa_retriever({"question": query, "chat_history": chat_history})
        return response

    @staticmethod
    def format_past_conversations(past_conversations):
        formatted_conversations = []
        for conversation in past_conversations:
            message_type = conversation.type
            if message_type not in ["user", "ai", "system", "human"]:
                raise ValueError(f"Unknown message type: {message_type}")

            formatted_conversations.append({"type": message_type, "content": conversation.content})
        return formatted_conversations
