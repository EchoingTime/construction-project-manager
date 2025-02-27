"""
@File Name: models.py
@Description: This file contains the database models for our application.
@Referenced: https://www.youtube.com/watch?v=dam0GPOAvVI&ab_channel=TechWithTim
"""

from . import db # Importing from current package, the website folder, the db object from
# our __init__.py!
from flask_login import UserMixin # Custom class that gives our user object specific things
# for flask login. Just helps a user login
from sqlalchemy.sql import func

class Note(db.Model): # A Database model is like a blueprint or layout for an object that 
# will be stored in the database. So all Notes must confirm to what is written here!
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # Gets current date and
    # time for us
    # Foreign key time! A Relationship between Note and User objects
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Must pass a valid user id to
    # this column when we create a note object. 1-to-many relationship

# Must define name of object inheriting from db.Model and UserMixin (class inside flask_login)
class User(db.Model, UserMixin): # Now to define our schema, the columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) # No user can have the same email as another
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') # Tells Flask and sqlAlchemy to do their magic, and when
    # ever we create a note, add to the user's note relationship, that note id