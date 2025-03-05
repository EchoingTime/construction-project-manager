"""
@File Name: views.py
@Description: This file contains the routes for handling the main application views, 
including rendering the home page, handling project creation, and deleting projects.
"""

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Project
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) # Main page of website
@login_required
def home():
    if request.method == 'POST':
        project = request.form.get('project')

        if len(project) < 1:
            flash('Project title is too short!', category='error')
        else:
            new_project = Project(data=project, user_id=current_user.id)
            db.session.add(new_project)
            db.session.commit()
            flash('Project created!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-project', methods=['POST'])
def delete_project():
    project = json.loads(request.data) # Takes in data from POST request and loads it as a Python dictonary of json object
    projectId = project['projectId'] # Accesses project id attribute
    project = Project.query.get(projectId) # Look for the project that has that id
    if project: # If note exists
        if project.user_id == current_user.id: # If we own that project
            db.session.delete(project) # Delete it
            db.session.commit()
    
    return jsonify({}) # Return empty response