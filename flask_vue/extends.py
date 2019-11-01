from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

migrate = Migrate()
sqlalchemy = SQLAlchemy()
cors = CORS()