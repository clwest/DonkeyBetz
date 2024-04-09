from flask_jwt_extended import JWTManager
from datetime import timedelta


import os
from dotenv import load_dotenv

load_dotenv()

jwt = JWTManager()


# Blacklist token check
def check_if_token_in_blacklist(jwt_header, jwt_payloader):
    from models.users import BlacklistedToken

    jti = jwt_payloader["jti"]
    token = BlacklistedToken.query.filter_by(token=str(jti)).first()
    return token is not None


def setup_jwt(app):
    jwt.init_app(app)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt.token_in_blocklist_loader(check_if_token_in_blacklist)
