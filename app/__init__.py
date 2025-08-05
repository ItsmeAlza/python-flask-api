from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .extensions import mail, db, jwt
from flask_restful import Api
from config import Config
from .errors import register_error_handlers
from app.resources.user import Users, User, Login, ChangePassword
from app.resources.email import SendEmail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    api = Api(app)

    api.add_resource(Users, '/api/users')
    api.add_resource(User, '/api/user/<int:id>')
    api.add_resource(SendEmail, '/api/send-email')
    api.add_resource(Login, '/api/login')
    api.add_resource(ChangePassword, '/api/change-password')

    register_error_handlers(app)
    mail.init_app(app)
    jwt.init_app(app)

    # @app.route('/')
    # def home():
    #     return '<h1>Flask</h1>'

    return app
