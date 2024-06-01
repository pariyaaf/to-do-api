from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from db import db
from os import environ 
from resources.user import blp as UserBlueprint
from datetime import timedelta




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
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    
    db.init_app(app)
    api = Api(app)
    migrate = Migrate(app, db)
    app.config["JWT_SECRET_KEY"] =  environ.get('JWT_SECRET')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
    jwt = JWTManager(app)

    api.register_blueprint(UserBlueprint)

    return app