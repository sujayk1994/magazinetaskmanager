from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.blueprints import auth, main, tasks, magazines, ads, cxo
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(tasks.bp)
    app.register_blueprint(magazines.bp)
    app.register_blueprint(ads.bp)
    app.register_blueprint(cxo.bp)
    
    return app

from app import models
