"""
@File Name: models.py
@Description: This file contains the database models for our application.
@Referenced: https://www.youtube.com/watch?v=dam0GPOAvVI&ab_channel=TechWithTim
"""

from . import db # Importing from current package, the website folder, the db object from __init__.py
from flask_login import UserMixin # Custom class that gives the user object specific things
# for flask login. Helps a user login
from sqlalchemy.sql import func

class Project(db.Model): # A Database model is like an object blueprint/layout that will be stored in the database. 
    # All Projects must confirm to what is written here.
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # Gets current date and time
    # Foreign key: A Relationship between Project and User objects
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Must pass a valid user id to
    # this column when we create a project object. 1-to-many relationship

# Must define name of object inheriting from db.Model and UserMixin (class inside flask_login)
class User(db.Model, UserMixin): # Define schema, the columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) # No user can have the same email as another
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    projects = db.relationship('Project') # Tells Flask and sqlAlchemy to do their magic, and when
    # ever we create a project, add to the user's project relationship, that project id