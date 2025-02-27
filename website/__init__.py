from flask import Flask
from flask_sqlalchemy import SQLAlchemy # Getting our database ready
from os import path
from flask_login import LoginManager # Manages the login aspects

db = SQLAlchemy() # Our database object
DB_NAME = "database.db"

def create_app(): # Initialize Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fdgajuttewfhb wefrwguyoioyu' 
    # Encrypt and secure session cookies
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(app.root_path, DB_NAME)}'
    # Need a file to store this in, SQL Light 3 will help! Will store this database in the
    # website folder
    db.init_app(app) # Initalizes the database! Takes the db and tells it which app we will
    # use with the database

    from .views import views # Got out blueprints imported
    from .auth import auth

    app.register_blueprint(views, url_prefix='/') # Register blueprints
    app.register_blueprint(auth, url_prefix='/') # Slash means no prefix

    from .models import User, Note # Must specify User and Note objects here

    with app.app_context(): # SQLAlchemny will not overwrite existing files
        db.create_all()

    login_manger = LoginManager()
    login_manger.login_view = 'auth.login' # Not logged in? where do we go...
    login_manger.init_app(app) # Tells manager what app we are using

    @login_manger.user_loader # Tells Flask how we load a user
    def load_user(id):
        return User.query.get(int(id)) # Knows it will look for primary key

    return app # Secret key is done

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')