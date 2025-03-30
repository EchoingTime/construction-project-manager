"""
@File Name: views.py
@Description: This file contains the routes for handling the main application views, 
including rendering the home page, handling project creation, and deleting projects.
"""

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Project, Message, User, Subcontractor, Assignment
from . import db
from datetime import datetime
import json

views = Blueprint('views', __name__)

# --------------------- Project Page ---------------------

# ----------- Project Creation -----------

# ChatGPT Assistance with page refreshing project duplications
@views.route('/', methods=['GET', 'POST']) # Main page of website
@login_required # Make sure to include this if a user must be logged in to view a page!
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

#------------ Project Viewing ------------

@views.route('/view-project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def view_project(project_id):
    project = Project.query.get(project_id)
    subcontractors = [assignment.subcontractor for assignment in project.subcontractors]
    return render_template("project.html", project=project, subcontractors=subcontractors, user=current_user)

# ----------- Project Deletion -----------

@views.route('/delete-project', methods=['POST'])
@login_required
def delete_project():
    project = json.loads(request.data) # Takes in data from POST request and loads it as a Python dictionary of json object
    projectId = project['projectId'] # Accesses project id attribute
    project = Project.query.get(projectId) # Look for the project that has that id
    if project: # If note exists
        if project.user_id == current_user.id: # If we own that project
            db.session.delete(project) # Delete it
            flash('Project was successfully deleted!', category='success')
            db.session.commit()
    
    return jsonify({}) # Return empty response

# ----------- Project Deadline Update -----------

# Route /update_deadline is needed for the html code, form --> action, to direct changes to
@views.route('/update_deadline/<int:project_id>', methods=['POST'])
@login_required
def update_deadline(project_id):
    project = Project.query.get(project_id)

    # Must be changed from a string to a valid date object for the database
    new_deadline_str = request.form.get('deadline') # Gets via input that has name='deadline'

    if new_deadline_str:
        project.deadline = datetime.strptime(new_deadline_str, "%Y-%m-%d").date()
    
    db.session.commit()
    flash('Deadline successfully updated!', category='success')
    return redirect(url_for('views.view_project', project_id=project_id, user=current_user))

# --------------------- Inbox Page ---------------------

@views.route('/inbox')
@login_required
def inbox():
    user_id = current_user.id 
    messages = Message.query.join(User, Message.sender_id == User.id).filter(Message.receiver_id == user_id).add_columns(Message.id, Message.message_text, Message.timestamp, User.email.label('sender_name')).order_by(Message.timestamp.desc()).all()
    return render_template("inbox.html", messages=messages)

# ----------- Sending Messages -----------

@views.route('/send_message', methods=['POST'])
@login_required
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
        flash("Message sent", category="success")
        return redirect(url_for("views.inbox"))
    else:
        flash("Something went wrong!", category="error")
    return render_template("inbox.html", messages=messages)

# -------------- Adding Subcontractors -----------

@views.route('/add-subcontractor/<int:project_id>', methods=['POST'])
@login_required
def add_subcontractor(project_id):
    if request.method == 'POST':
        subcontractor_name = request.form.get('subcontractor_name')
        subcontractor_email = request.form.get('subcontractor_email')
        subcontractor_trade = request.form.get('subcontractor_trade')

        if len(subcontractor_name) < 1 or len(subcontractor_email) < 1:
            flash('Subcontractor name and email required!', category='error')
        else:
            existing_subcontractor = Subcontractor.query.filter_by(email=subcontractor_email).first()
            if existing_subcontractor is None:
                flash("This subcontractor is not registered!", category='error')
                return redirect(request.referrer)
            #checks if the subcon has been assigned to THIS project already
            existing_assignment = Assignment.query.filter_by(project_id=project_id,subcontractor_id=existing_subcontractor.id).first()
            
            if existing_assignment:
                flash("This subcontractor is already assigned to this project!", category='error')
            else:
                new_assignment=Assignment(project_id=project_id,subcontractor_id=existing_subcontractor.id,assigned_date=datetime.now(),status="Incomplete")
                db.session.add(new_assignment)
                db.session.commit()
                flash('Subcontractor Added!', category='success')

            project=Project.query.get(project_id) #get project before rendering template
            return redirect(url_for('views.view_project', project_id=project_id))
            #return redirect(url_for('views.project', project_id=project_id))
            


