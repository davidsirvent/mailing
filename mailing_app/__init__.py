from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .main import main

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'my-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    app.register_blueprint(main)

    # db rebuild
    @app.route('/db-rebuild')
    def db_create():
        from .models import Config
        db.drop_all()
        db.create_all(app=create_app())
        return 'db rebuild'

    return app
