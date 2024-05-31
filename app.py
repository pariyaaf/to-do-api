from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from db import db
from os import environ 


def create_app():

    load_dotenv()

    app = Flask(__name__)
    app.config["API_TITLE"] = "TO DO API"
    app.config["API_VERSION"] = "v1.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] ="/swagger-ui"
    app.config[
            "OPENAPI_SWAGGER_UI_URL"
        ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLACHEMY_DATABASE_URL"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    
    db.init_app(app)
    api = Api(app)
    migrate = Migrate(app, db)
    app.config["JWT_SECRET_KEY"] =  environ.get('JWT_SECRET')
    jwt = JWTManager(app)


    return app