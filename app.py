from flask import Flask, jsonify, send_from_directory
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_uploads import configure_uploads, patch_request_class
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint

from blocklist import BLOCKLIST
from db import db
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.user import blp as UserBlueprint
from resources.image import blp as ImageBlueprint
from libs.image_helper import IMAGE_SET
import default_config


def create_app():
    app = Flask(__name__)

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Seans-Python-Flask-REST-Boilerplate"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    load_dotenv(".env", verbose=True)
    # app.config.from_object("default_config")
    app.config.from_envvar("APPLICATION_SETTINGS")

    db.init_app(app)
    patch_request_class(app, 10 * 1024 * 1024)  # limit the maximum size of image (10MB)
    configure_uploads(app, IMAGE_SET)  # if we have multiple set then we can call it multiple times
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "abc"
    jwt = JWTManager(app)

    # db.create_all()
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_paylaod):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_loader, jwt_payload):
        return (
            jsonify(
                {"description": "The token is not fresh.", "error": "fresh_token_required"}
            ),
            401
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_paylaod):
        return (
            jsonify({"message": "The token has expired.", "error": "token_exoired"}), 401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"message": "Signature verification failed", "error": "invalid_token"}), 401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"message": "Request does not contain an access token.", "error": "authentication_required"}), 401,
        )

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ImageBlueprint)

    return app


app = create_app()
app.run(port=5000, debug=False)
