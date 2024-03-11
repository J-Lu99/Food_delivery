from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import Product, User
from exts import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required
from products import product_ns
from auth import auth_ns

def create_app(config):
    app=Flask(__name__)
    app.config.from_object(DevConfig)
    api=Api(app, doc='/docs')
    api.add_namespace(product_ns)
    api.add_namespace(auth_ns)

    db.init_app(app)

    migrate=Migrate(app,db)
    JWTManager(app)

# this creates a default namespace
    @api.route('/hello')
    class HelloResource(Resource):
        def get(self):
            return jsonify('hello world')

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'Product':Product,
            'user':User
        }
    return app