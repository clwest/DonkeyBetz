import unittest
from app import create_app, db
from models.users import User
from models.chatbots import Chatbot

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_chatbot(self):
        user = User(username="testuser", email="test@example.com")
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/api/chatbot/create', json={
            'name': 'testbot',
            'description': 'A test chatbot'
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], 'testbot')

if __name__ == '__main__':
    unittest.main()