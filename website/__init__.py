"""
@File Name: __init__.py
@Description: This file contains the initialization of the Flask app, configuration of the database, 
and user authentication setup. It imports the necessary routes, manages the blueprints, 
and handles database creation for the application.
"""

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy # Readying Database
from flask_login import LoginManager # Manages the login aspects
from flask_migrate import Migrate # Updates the db to have a new column w/o losing data
from flask_mail import Mail # For sending emails
from os import path

migrate=Migrate()
db = SQLAlchemy() # Database object
DB_NAME = "database.db"
mail=Mail() # Initialize Flask-Mail

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
    from .file_upload import file_upload

    app.register_blueprint(views, url_prefix='/') # Register blueprints
    app.register_blueprint(auth, url_prefix='/') # Slash means no prefix
    app.register_blueprint(file_upload, url_prefix='/')

    from .models import User # Must specify user here

    # With app.app_context(): # SQLAlchemny will not overwrite existing files
    # db.create_all()

    login_manger = LoginManager()
    login_manger.login_view = 'auth.login' # Not logged in? Where do we go...
    login_manger.init_app(app) # Tells manager what app we are using

    @login_manger.user_loader # Tells Flask how we load a user
    def load_user(id):
        return User.query.get(int(id)) # Knows it will look for primary key

    @login_manger.unauthorized_handler
    def unauthorized():
        return redirect(url_for('auth.login'))

    from .context_processors import unread_message_count
    app.context_processor(lambda: {'unread_message_count': unread_message_count()})

    from flask_login import current_user
    from .models import File, Project

    @app.context_processor
    def inject_new_invoice_count():
        if current_user.is_authenticated and current_user.role == 'contractor':
            assigned_projects = Project.query.filter_by(user_id=current_user.id).all()
            new_invoice_count = sum(
                1 for project in assigned_projects
                for invoice in File.query.filter_by(project_id=project.id, is_invoice=True).all()
                if invoice.is_new
            )
            return {'new_invoice_count': new_invoice_count}
        return {'new_invoice_count': 0}

    return app # Secret key is done

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
        # Must import all models before creating tables
            from .models import User, Project, Task, Subcontractor, Message, Assignment, File
            db.create_all()
            print('Created Database!')