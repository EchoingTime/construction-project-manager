"""
@File Name: views.py
@Description: This file contains the routes for handling the main application views, 
including rendering the home page, handling project creation, and deleting projects.
"""

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from .models import File, Project, Message, User, Subcontractor, Assignment, Task
from . import db
from datetime import datetime
from flask_mail import Mail, Message
from website import mail
from flask import current_app
import json

views = Blueprint('views', __name__)

# --------------------- / will send user to views home (beneath this code segment) ---------------------

@views.route('/')
def redirect_to_home():
    return redirect(url_for('views.home'))

# --------------------- Home Pages & Project Creation ---------------------

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    # For Handling POST (Project Creation on the Project Overview Page (aka home.html))
    if request.method == 'POST' and current_user.role == "contractor":
        project = request.form.get('project')

        if not project or len(project.strip()) < 1:
            flash('Project needs a descriptive title!', category='error')
        else:
            # Check if project already exists for this user
            existing_project = Project.query.filter_by(project_name=project, user_id=current_user.id).first()
            if existing_project:
                flash("This project already exists!", category='error')
            else:
                # Create and save it
                new_project = Project(project_name=project, user_id=current_user.id)
                db.session.add(new_project)
                db.session.commit()
                flash('Created New Project', category='success') 
        # Redirect to the same page (prevents form re-submission via freshing page - ChatGPT Assist)
        return redirect(url_for('views.home'))

    # Handles GET (rendering the actual home.html and homeSub.html pages)
    if current_user.role == "contractor": # Goes to contractor page
        return render_template("home.html", user=current_user)
    elif current_user.role == "subcontractor":
        subcontractor = Subcontractor.query.filter_by(email=current_user.email).first()
        assignments = Assignment.query.filter_by(subcontractor_id=subcontractor.id).all() 
        assigned_projects = db.session.query(Assignment.project_id).filter_by(subcontractor_id=subcontractor.id).all()
        project_ids = [project[0] for project in assigned_projects]
        projects = db.session.query(Project).filter(Project.id.in_(project_ids)).all()
        return render_template("homeSub.html", user=current_user, assignments=assignments, projects=projects)
    else:
        return "Unauthorized", 403

#------------ Project Viewing ------------

@views.route('/view-project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def view_project(project_id):
    project = Project.query.get(project_id)
    subcontractors = [assignment.subcontractor for assignment in project.subcontractors]
    tasks = Task.query.filter_by(project_id=project_id).all()
    return render_template("project.html", project=project, subcontractors=subcontractors, user=current_user, tasks=tasks)

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

# ----------- Edit Project Name -----------

@views.route('/edit-project-name', methods=['POST'])
@login_required
def edit_project_name():
    project_name = request.form.get('project_name')
    project_id = request.args.get('project_id') # Will retrieve the project id from the URL

    project = Project.query.get(project_id)

    if project and project.user_id == current_user.id:
        project.project_name = project_name
        db.session.commit()
        flash("Project name updated successfully!", category='success')
    
    return redirect(url_for('views.view_project', project_id=project_id))

# ----------- Subcontractor Assignment Deletion -----------

@views.route('/delete-assignment', methods=['POST'])
@login_required
def deleteAssignment():
    data = json.loads(request.data)
    subcontractor_id = data['subcontractorId']
    assignment = Assignment.query.filter_by(subcontractor_id=subcontractor_id).first() 

    if assignment and assignment.project.user_id == current_user.id: 
        db.session.delete(assignment) 
        db.session.commit()
        flash('Subcontractor assignment was successfully removed!', category='success')
    
    return jsonify({}) 

# ----------- Task Deletion -----------

@views.route('/delete-task', methods=['POST'])
@login_required
def deleteTask():
    data = json.loads(request.data) # Get JSON data from the client
    task_id = data['taskId'] # Access the task ID

    task = Task.query.get(task_id) # Find the task by ID

    if task and task.project.user_id == current_user.id: 
        db.session.delete(task) 
        db.session.commit()
        flash('Task was successfully deleted!', category='success')
    
    return jsonify({}) # Return empty = indicates success

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
    unread_messages = Message.query.filter_by(receiver_id=user_id, is_read=False).all()

    for message in unread_messages:
        message.is_read = True
    db.session.commit()

    unread_count = len(unread_messages)
    return render_template("inbox.html", messages=messages, unread_count=unread_count)

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

# --------------------- Invoice ---------------------

@views.route('/upload_invoice/<int:project_id>', methods=['POST'])
@login_required
def upload_invoice(project_id):
    if 'invoice' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['invoice']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        new_file = File(
            filename=file.filename,
            data=file.read(),
            project_id=project_id,
            is_invoice=True
        )
        db.session.add(new_file)
        db.session.commit()

        # Send message to contractor
        contractor = User.query.filter_by(role='contractor').first()
        if contractor:
            new_message = Message(
                sender_id=current_user.id,
                receiver_id=contractor.id,
                message_text=f'Invoice uploaded for project {project_id}: {file.filename}'
            )
            db.session.add(new_message)
            db.session.commit()

        flash('Invoice successfully uploaded and sent to contractor')
        return redirect(url_for('views.view_project', project_id=project_id))

# --------------------- Add Task ---------------------

@views.route('/add_task/<int:project_id>', methods=['POST'])
@login_required
def add_task(project_id):
    # Get the project
    project = Project.query.get(project_id)
    if not project:
        flash('Project not found!', category='error')
        return redirect(url_for('views.home'))

    # Get form data
    task_name = request.form.get('task-name')
    task_description = request.form.get('task-description')  # New description field
    task_deadline = request.form.get('task-deadline')
    task_completion = request.form.get('task-completion')  # Replaces "status"
    subcontractor_id = request.form.get('task-subcontractor')  # Get subcontractor ID

    # Validate form data
    if not task_name or not task_deadline or not task_completion:
        flash('All fields except description are required to create a task!', category='error')
        return redirect(url_for('views.view_project', project_id=project_id))

    # Create a new task
    new_task = Task(
        project_id=project_id,
        name=task_name,
        description=task_description,  # Add description
        deadline=datetime.strptime(task_deadline, "%Y-%m-%d").date(),
        completion=task_completion,  # Replace "status" with "completion"
        date_created=datetime.now(),
        subcontractor_id=subcontractor_id  # Add subcontractor ID
    )
    db.session.add(new_task)
    db.session.commit()

    flash('Task successfully added!', category='success')
    return redirect(url_for('views.view_project', project_id=project_id))

# --------------------- Profile ---------------------

@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)

# --------------------- Assigned Tasks ---------------------

@views.route('/assigned_tasks')
@login_required
def assigned_tasks():
    # Ensure the current user is a subcontractor
    subcontractor = Subcontractor.query.filter_by(user_id=current_user.id).first()
    if not subcontractor:
        return "You are not authorized to view this page.", 403

    # Get tasks assigned to the subcontractor
    tasks = subcontractor.get_assigned_tasks()
    return render_template('assigned_tasks.html', tasks=tasks)

# --------------------- Project Tasks ---------------------

@views.route('/project/<int:project_id>/tasks')
@login_required
def view_project_tasks(project_id):
    # Fetch the project and its associated tasks
    project = Project.query.get_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project_id).all()
    return render_template('project_tasks.html', project=project, tasks=tasks)

# --------------------- Send Email Ping ---------------------

@views.route('/send_ping/<int:project_id>', methods=['POST'])
def send_ping(project_id):
    project = Project.query.get(project_id)
    contractor = User.query.get(project.user_id)

    reason = request.form['reason']
    msg = Message(subject=f"[Ping] {reason} {current_user.first_name} on {project.project_name}",
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[contractor.email],
                  body=(f"You've received a ping from {current_user.first_name}"
                        f"(email: {current_user.email})\n\n"
                        f"Project: {project.project_name}\n"
                        f"Reason: {reason}\n\n"))
    mail.send(msg)
    return redirect(url_for('views.view_project', project_id=project_id))

