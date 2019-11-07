from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

migrate = Migrate()
db = SQLAlchemy()  # flask db migrate -m "x" flask db upgrade flask db downgrade 命令可以回滚上次的迁移 
cors = CORS()