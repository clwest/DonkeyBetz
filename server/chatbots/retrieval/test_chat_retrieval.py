import unittest
from unittest.mock import MagicMock
from chat_retrieval import ChatRetrievalLLM

class TestChatRetrievalLLM(unittest.TestCase):
    def setUp(self):
        self.chat_retrieval = ChatRetrievalLLM()

    def test_llm_query(self):
        query = "How are you?"
        formatted_chat_history = [
            {"type": "user", "content": "Hello"},
            {"type": "ai", "content": "Hi, how can I help you?"},
        ]
        collection_name = "conversations"

        # Mock the necessary dependencies
        self.chat_retrieval.embeddings = MagicMock()
        self.chat_retrieval.retriever = MagicMock()
        self.chat_retrieval.qa_retriever = MagicMock()

        # Call the method under test
        response = self.chat_retrieval.llm_query(query, formatted_chat_history, collection_name)

        # Assert the expected response
        self.assertIsNotNone(response)

    def test_format_past_conversations(self):
        past_conversations = [
            MagicMock(type="user", content="Hello"),
            MagicMock(type="ai", content="Hi, how can I help you?"),
        ]

        # Call the method under test
        formatted_conversations = ChatRetrievalLLM.format_past_conversations(past_conversations)

        # Assert the expected formatted conversations
        self.assertEqual(len(formatted_conversations), 2)
        self.assertEqual(formatted_conversations[0]["type"], "user")
        self.assertEqual(formatted_conversations[0]["content"], "Hello")
        self.assertEqual(formatted_conversations[1]["type"], "ai")
        self.assertEqual(formatted_conversations[1]["content"], "Hi, how can I help you?")

if __name__ == "__main__":
    unittest.main()