"""
@File Name: views.py
@Description: This file contains the routes for handling the main application views, 
including rendering the home page, handling project creation, and deleting projects.
"""

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Project, Message, User
from . import db
import json

views = Blueprint('views', __name__)

# --------------------- Project Page ---------------------

# ----------- Project Creation -----------

# ChatGPT Assistance with page refreshing project dublications
@views.route('/', methods=['GET', 'POST']) # Main page of website
@login_required
def project():
    if request.method == 'POST':
        project = request.form.get('project')

        if len(project) < 1: # If project does not have a title, flash an error while preventing creation
            flash('Project needs a descriptive title!', category='error')
        else:
            # Check if project already exists
            existing_project = Project.query.filter_by(project_name=project, user_id=current_user.id).first()
            if existing_project:
                flash("This project already exists!", category='error')
            else:
                # Create and save it
                new_project = Project(project_name=project, user_id=current_user.id)
                db.session.add(new_project)
                db.session.commit()
                flash('Created New Project', category='success')
            
        # Redirect to the same page (prevents form re-submission via freshing page)
        return redirect(url_for('views.project'))

    # Renders the page consisting of the user's projects
    return render_template("home.html", user=current_user)

# ----------- Project Deletion -----------

@views.route('/delete-project', methods=['POST'])
def delete_project():
    project = json.loads(request.data) # Takes in data from POST request and loads it as a Python dictonary of json object
    projectId = project['projectId'] # Accesses project id attribute
    project = Project.query.get(projectId) # Look for the project that has that id
    if project: # If note exists
        if project.user_id == current_user.id: # If we own that project
            db.session.delete(project) # Delete it
            flash('Deleted Project', category='success')
            db.session.commit()
    
    return jsonify({}) # Return empty response

# --------------------- Inbox Page ---------------------

@views.route('/inbox')
def inbox():
    user_id = current_user.id 
    messages = Message.query.join(User, Message.sender_id == User.id).filter(Message.receiver_id == user_id).add_columns(Message.id, Message.message_text, Message.timestamp, User.email.label('sender_name')).order_by(Message.timestamp.desc()).all()
    return render_template("inbox.html", messages=messages)

# ----------- Sending Messages -----------

@views.route('/send_message', methods=['POST'])
def send_message():
    sender_id = current_user.id
    receiver_name = request.form['receiver_email']
    content = request.form['content']
    receiver = User.query.filter_by(email=receiver_name).first()

    if receiver:
        receiver_id = receiver.id
        messages = Message(sender_id=sender_id, receiver_id=receiver_id, message_text=content)
        db.session.add(messages)
        db.session.commit()
        flash("Message sent", category="seccess")
        return redirect(url_for("views.inbox"))
    else:
        flash("Something went wrong!", category="error")
    return render_template("inbox.html", messages=messages)
