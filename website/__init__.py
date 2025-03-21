"""
@File Name: __init__.py
@Description: This file contains the initialization of the Flask app, configuration of the database, 
and user authentication setup. It imports the necessary routes, manages the blueprints, 
and handles database creation for the application.
"""

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy # Readying Database
from os import path
from flask_login import LoginManager # Manages the login aspects
from flask_migrate import Migrate #updates the db to have a new column w/o losing data

migrate=Migrate()

db = SQLAlchemy() # Database object
DB_NAME = "database.db"

def create_app(): # Initialize Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fdgajuttewfhb wefrwguyoioyu' 
    # Encrypt and secure session cookies
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(app.root_path, DB_NAME)}'
    # Need a file to store this in, SQL Light 3 will store this database in the website folder
    db.init_app(app) # Initalizes the database. Takes the database and tells it which app we will use with the database
    migrate.init_app(app,db)
    from .views import views # Got blueprints imported
    from .auth import auth

    app.register_blueprint(views, url_prefix='/') # Register blueprints
    app.register_blueprint(auth, url_prefix='/') # Slash means no prefix

    from .models import User, Project # Must specify User and Project objects here

    #with app.app_context(): # SQLAlchemny will not overwrite existing files
   #     db.create_all()

    login_manger = LoginManager()
    login_manger.login_view = 'auth.login' # Not logged in? Where do we go...
    login_manger.init_app(app) # Tells manager what app we are using

    @login_manger.user_loader # Tells Flask how we load a user
    def load_user(id):
        return User.query.get(int(id)) # Knows it will look for primary key

    @login_manger.unauthorized_handler
    def unauthorized():
        return redirect(url_for('auth.login'))

    return app # Secret key is done

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')