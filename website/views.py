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

# --------------------- Home Pages ---------------------

@views.route('/home')
@login_required
def home():
    if current_user.role == "contractor": # Goes to contractor page
        return render_template("home.html", user=current_user)
    elif current_user.role == "subcontractor":
        # Query the subcontractor
        #subcontractor = Subcontractor.query.filter_by(email=current_user.email).first()
       #assignments = Assignment.query.filter_by(subcontractor_id=subcontractor.id).all()
        #project_ids = [assignment.project_id for assignment in assignments]
        #assigned_projects = Project.query.filter(Project.id.in_(project_ids)).all()
        #return render_template("homeSub.html", subcontractor=subcontractor,user=current_user, assigned_projects=assigned_projects)
        return render_template("homeSub.html", user=current_user)
    else:
        return "Unauthorized", 403

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
    #if current_user.role != "subcontractor":
        return redirect(url_for('views.project'))
    
   
    if current_user.role != "subcontractor":
        return render_template("home.html", user=current_user)
    else:
        subcontractor = Subcontractor.query.filter_by(email=current_user.email).first()
        assignments = Assignment.query.filter_by(subcontractor_id=subcontractor.id).all() 
        assigned_projects = db.session.query(Assignment.project_id).filter_by(subcontractor_id=subcontractor.id).all()
        project_ids = [project[0] for project in assigned_projects]
        projects = db.session.query(Project).filter(Project.id.in_(project_ids)).all()
        return render_template("homeSub.html", user=current_user, assignments=assignments, projects=projects)

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

# ----------- Project Filter -----------

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

# ----------- Project Completion Status Update -----------

# Note: In the Project table, the column is called progress and not status.
@views.route('/update_project_completion_status/<int:project_id>', methods=['POST'])
@login_required
def update_project_completion_status(project_id):
    project = Project.query.get(project_id)

    new_status = request.form.get('project-status')

    if new_status: # To ensure an option was selected
        project.progress = new_status
        db.session.commit()
        flash('Completion Status successfully updated!', category='success')
    else:
        flash('No status selected!', category='error')
    return redirect(url_for('views.view_project', project_id=project_id, user=current_user))

# ----------- Project Add Subcontractor -----------

@views.route('/views.add_subcontractor/<int:project_id>', methods=['POST'])
@login_required
def add_subcontractor(project_id):
    # Obtain what user filled inside the Subcontractor form
    form_email = request.form.get('subcontractor-email')

    # Query all users that have the role "subcontractor" and extract the associated emails
    valid_user_email = [user.email for user in User.query.filter_by(role='subcontractor').all()]
    
    if form_email not in valid_user_email:
        flash('This is not a valid subcontractor email!', category='error')
        return redirect(url_for('views.view_project', project_id=project_id))
    
    # Query for subcontractor's ID from the Subcontractor Table
    subcontractor = Subcontractor.query.filter_by(email=form_email).first()

    if not subcontractor:
        flash('Subcontractor does not exist!', category='error')
        return redirect(url_for('views.view_project', project_id=project_id))

    # Checks if the subcontractor has been assigned to THIS project already
    existing_project_assignment = Assignment.query.filter_by(project_id=project_id, subcontractor_id=subcontractor.id).first()

    if existing_project_assignment:
        flash('This subcontractor is already assigned to this project!', category='error')
    else:
        new_assignment = Assignment(project_id=project_id, subcontractor_id = subcontractor.id, assigned_date=datetime.now(), status='Incomplete')
        db.session.add(new_assignment)
        db.session.commit()
        flash('Subcontractor Assigned!', category='success')
    return redirect(url_for('views.view_project', project_id=project_id))

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

# -------------- Add Address -------------

@views.route('/update_address/<int:project_id>', methods=['POST'])
def update_address(project_id):
    project=Project.query.get(project_id)
    new_address=request.form.get('project_address')
    if new_address:
        project.address=new_address
        db.session.commit()
    return redirect(url_for('views.view_project', project_id=project_id))
 
# ---------------- Subcontractor Projects --------------

#@views.route('/subcontractor_projects')
#def subcontractor_projects():
#    subcontractor = Subcontractor.query.filter_by(email=current_user.email).first()
    
#    assignments=Assignment.query.filter_by(subcontractor_id=subcontractor.id).all()
#    assigned_projects=[assignment.project for assignment in assignments]
#    return render_template('homeSub.html', assigned_projects=assigned_projects)

# ---------------- Subcontractor Home ------------------
#@views.route("/home_Sub")
#def home_sub():
 #   subcontractor = Subcontractor.query.filter_by(email=current_user.email).first()
    
 #   if not subcontractor:
 #       flash('Subcontractor does not exist!', category='error')
 #       return redirect(url_for('views.home'))
 #   assignments = Assignment.query.filter_by(subcontractor_id=subcontractor.id).all()
 #   assigned_projects = [assignment.project for assignment in assignments]
    

  #  return render_template("homeSub.html", user=current_user, assigned_projects=assigned_projects, subcontractor=subcontractor)

# --------------------- Calendar ---------------------

@views.route('/calendar')
@login_required
def calendar():
    return render_template("calendar.html", user=current_user)
    