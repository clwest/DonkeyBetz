from flask_cors import CORS

def configure_cors(app):
  # CORS configuration
  CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})