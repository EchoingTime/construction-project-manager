"""
@File Name: models.py
@Description: This file contains the database models for our application.
@Important: Read Important comment below before making changes here.
"""

from . import db # Importing from current package, the website folder, the db object from __init__.py
from flask_login import UserMixin # Custom class that gives the user object specific things
from sqlalchemy.sql import func

# IMPORTANT BEFORE ADDING/CHANGING MODELS! Go to README.md and read instructions under Database Modifications

# --------------------- User Table ---------------------

# Must define name of object inheriting from db.Model and UserMixin (class inside flask_login)
class User(db.Model, UserMixin): # Define schema, the columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) # No user can have the same email as another
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(150))
    projects = db.relationship('Project') # Tells Flask and sqlAlchemy to do their magic, and when creating a project, 
    # add to the user's project relationship, that project id

# --------------------- Project Table ---------------------

class Project(db.Model): # Database model: An object blueprint/layout that will be stored in the database 
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(70))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # Gets current date and time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 1-to-many relationship

# --------------------- Message Table ---------------------

class Message(db.Model): #Model to handle the messages
    id = db.Column(db.Integer, primary_key=True)   #store all messages in a table 
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id')) #used to fetch the correct messages based on who received and who sent
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message_text = db.Column(db.Text, nullable = False)
    timestamp = db.Column(db.DateTime, default = db.func.current_timestamp())

