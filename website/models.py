"""
@File Name: models.py
@Description: This file contains the database models for our application.
@Referenced: https://www.youtube.com/watch?v=dam0GPOAvVI&ab_channel=TechWithTim
"""

from . import db # Importing from current package, the website folder, the db object from __init__.py
from flask_login import UserMixin # Custom class that gives the user object specific things
from sqlalchemy.sql import func

class Project(db.Model): # Database model: An object blueprint/layout that will be stored in the database 
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # Gets current date and time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 1-to-many relationship

# Must define name of object inheriting from db.Model and UserMixin (class inside flask_login)
class User(db.Model, UserMixin): # Define schema, the columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) # No user can have the same email as another
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    projects = db.relationship('Project') # Tells Flask and sqlAlchemy to do their magic, and when creating a project, 
    # add to the user's project relationship, that project id