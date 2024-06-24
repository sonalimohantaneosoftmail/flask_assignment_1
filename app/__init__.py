from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
# from celery import Celery
from flasgger import Swagger
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
swagger = Swagger()
# celery = Celery(__name__, broker='redis://redis:6379/0')

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)
    
    # with app.app_context():
    #     from .views import auth, data
    #     app.register_blueprint(auth.bp)
    #     app.register_blueprint(data.bp)

    from app.views.auth import main_data as auth_bp
    from app.views.data import main_data as data_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(data_bp)
        
    return app

# def make_celery(app):
#     celery.conf.update(app.config)
#     return celery

# celery = make_celery(create_app())
