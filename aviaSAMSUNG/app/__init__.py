from flask import Flask
from app.requests import module

def create_app():
    app = Flask(__name__)
    app.register_blueprint(module)
    app.secret_key = 'my_secret_key'
    return app

yourapp = create_app()