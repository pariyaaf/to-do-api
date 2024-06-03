from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from db import db
from os import environ 
from resources.user import blp as UserBlueprint
from datetime import timedelta
from flask_caching import Cache
from blocklist import BLOCKLIST


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
    
    cache = Cache(config={"CACHE_TYPE" : "simple"})

    db.init_app(app)
    cache.init_app(app)

    # app.config["CACHE"] = cache

    # app.cache = cache

    api = Api(app)
    migrate = Migrate(app, db)

    app.config["JWT_SECRET_KEY"] =  environ.get('JWT_SECRET')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
    jwt = JWTManager(app)


    @jwt.token_in_blocklist_loader
    def check_blacklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has been revoked.", "error": "token_revoked"}),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {'is_admin': False}
        
    api.register_blueprint(UserBlueprint)

    return app