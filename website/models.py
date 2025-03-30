"""
@File Name: models.py
@Description: This file contains the database models for our application.
@Important: Read Important comment below before making changes here.
"""

from . import db # Importing from current package, the website folder, the db object from __init__.py
from flask_login import UserMixin # Custom class that gives the user object specific things
from sqlalchemy.sql import func
from sqlalchemy import Enum # Allows the restriction of a column's values to a set of options

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
    # Migrations includes default value below v (progress)
    progress = db.Column(Enum('Not Yet Started', 'On Hold', 'In Progress', 'Completed', 'Canceled', name='progress_status'), nullable=False, default='Not Yet Started') # Project's Progress: Not Yet Started (Blue) | On Hold (Orange) | In Progress (Yellow) | Completed (Green) | Canceled (Red)
    deadline = db.Column(db.Date, nullable=True) # Project Deadline

    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 1-to-many relationship

    subcontractors = db.relationship('Assignment', back_populates='project') #many to many relation
    tasks = db.relationship('Task', backref='project', lazy='dynamic') # 1-to-many relationship

# --------------------- Task Table ---------------------

class Task(db.Model): # Model to allow contractors to assign tasks
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.Date, nullable=True) # Task Deadline
    completion = db.Column(Enum('Completed', 'In Progress', 'Canceled', name='completion_status'), nullable=False, default='In Progress')

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False) # Foreign Key

# --------------------- Message Table ---------------------

class Message(db.Model): #Model to handle the messages
    id = db.Column(db.Integer, primary_key=True) #store all messages in a table 
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id')) #used to fetch the correct messages based on who received and who sent
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message_text = db.Column(db.Text, nullable = False)
    timestamp = db.Column(db.DateTime, default = db.func.current_timestamp())

#--------------------- Subcontractor Table ------------------

class Subcontractor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True, nullable=False)
    trade = db.Column(db.String(150))

#--------------------- Assignment Table ----------------------

class Assignment(db.Model): #helper table for Subcontractor-Project Relationship
    id = db.Column(db.Integer,primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    subcontractor_id = db.Column(db.Integer, db.ForeignKey('subcontractor.id'))
    assigned_date = db.Column(db.DateTime, default=func.now())
    status = db.Column(db.String(50), default='Incomplete')
    project = db.relationship('Project', back_populates='subcontractors')
    subcontractor = db.relationship('Subcontractor', backref=db.backref('assignments', lazy='dynamic'))
 
