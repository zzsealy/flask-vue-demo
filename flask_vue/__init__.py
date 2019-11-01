from flask import Flask
from flask_vue.extends import cors, sqlalchemy, migrate
from config import Config
from flask_vue.api import bp as api_bp
from flask_sqlalchemy import SQLAlchemy 

def create_app(config_class=Config):
    app = Flask(__name__)
    config_app(app, config_class)
    register_extends(app)
    register_blueprint(app)
    # 注册蓝本
    return app


def register_extends(app):
    cors.init_app(app)
    sqlalchemy.init_app(app)
    migrate.init_app(app)


def register_blueprint(app):
    app.register_blueprint(api_bp, url_prefix = '/api')


def config_app(app, config_class):
    app.config.from_object(config_class)
