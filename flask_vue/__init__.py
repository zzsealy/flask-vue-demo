from flask import Flask
from flask_vue.extends import cors, db, migrate
from flask_vue.models import User
from config import Config
from flask_vue.api import bp as api_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    config_app(app, config_class)
    register_extends(app)
    register_blueprint(app) # 注册蓝本
    register_shell_context(app)
    return app


def register_extends(app):
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprint(app):
    app.register_blueprint(api_bp, url_prefix = '/api')


def config_app(app, config_class):
    app.config.from_object(config_class)

# 注册上下文
def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User)
    

from flask_vue import models