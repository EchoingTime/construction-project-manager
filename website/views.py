"""
@File Name: views.py
@Description: This file contains the routes for handling the main application views, 
including rendering the home page, handling project creation, deleting projects, etc.
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
    project_files = File.query.filter_by(project_id=project_id, is_invoice=False).all()
    return render_template("project.html", project=project, subcontractors=subcontractors, user=current_user, tasks=tasks, project_files=project_files)

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

# --------------------- Calendar ---------------------

@views.route('/calendar')
@login_required
def calendar():
    # Find out if the user is a subcontractor or contractor
    subcontractor = Subcontractor.query.filter_by(email=current_user.email).first()

    # If a subcontractor...
    if subcontractor:
        # Retrieve assigned projects or tasks assigned in the project
        assigned_project_ids = [a.project_id for a in subcontractor.assignments]
        user_projects = Project.query.filter(Project.id.in_(assigned_project_ids)).all()

        # Filter tasks assigned to this subcontractor
        user_projects_json = [
            {
                "id": project.id,
                "project_name": project.project_name,
                "deadline": project.deadline.isoformat() if project.deadline else None,
                "status": (project.progress or "in progress").lower(),
                "tasks": [
                    {
                        "id": task.id,
                        "name": task.name,
                        "deadline": task.deadline.isoformat() if task.deadline else None,
                        "status": (task.completion or "in progress").lower()
                    }
                    for task in project.tasks
                    if task.subcontractor_id == subcontractor.id
                ]
            }
            for project in user_projects
        ]
    else:
        # For users whose role is a contractor
        user_projects = Project.query.filter(
            (Project.user_id == current_user.id) |
            (Project.subcontractors.any(subcontractor_id=current_user.id))
        ).all()

        user_projects_json = [
            {
                "id": project.id,
                "project_name": project.project_name,
                "deadline": project.deadline.isoformat() if project.deadline else None,
                "status": (project.progress or "in progress").lower(),
                "tasks": [
                    {
                        "id": task.id,
                        "name": task.name,
                        "deadline": task.deadline.isoformat() if task.deadline else None,
                        "status": (task.completion or "in progress").lower()
                    }
                    for task in project.tasks
                ]
            }
            for project in user_projects
        ]

    return render_template("calendar.html", user=current_user, user_projects_json=user_projects_json)

# --------------------- Invoice ---------------------

@views.route('/upload_invoice/<int:project_id>', methods=['POST'])
@login_required
def upload_invoice(project_id):
    if 'invoice' not in request.files:
        flash('No file part', category='error')
        return redirect(request.url)

    file = request.files['invoice']
    if file.filename == '':
        flash('No selected file', category='error')
        return redirect(request.url)

    if file:
        new_file = File(
            filename=file.filename,
            data=file.read(),
            project_id=project_id,
            is_invoice=True,
            is_new=True  # Mark as new
        )
        db.session.add(new_file)
        db.session.commit()
        flash('Invoice successfully uploaded', category='success')
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
    subcontractor_id = request.form.get('task-subcontractor')  # Get subcontractor ID

    # Default task completion to "Not Started" for all users
    #task_completion = "Not Started"
    task_completion = "Incomplete"
    # Validate form data
    if not task_name or not task_deadline:
        flash('Task name and deadline are required to create a task!', category='error')
        return redirect(url_for('views.view_project', project_id=project_id))

    # Create a new task
    new_task = Task(
        project_id=project_id,
        name=task_name,
        description=task_description,  # Add description
        deadline=datetime.strptime(task_deadline, "%Y-%m-%d").date(),
        completion=task_completion,  # Default to "Not Started"
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
    # Need to add a reference to get subcontractor info, if user is a subcontractor
    subcontractor = Subcontractor.query.filter_by(email=current_user.email).first()
    return render_template("profile.html", user=current_user, subcontractor=subcontractor)

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

# ----------------------- Subcontractor Search Bar -----------------------

@views.route('/search_subcontractors')
def search_subcontractors():
    query = request.args.get('q','')
    results = Subcontractor.query.filter(Subcontractor.email.ilike(f"%{query}%")).all()
    users = [{'id': sub.id, 'email': sub.email} for sub in results]
    return jsonify(users)

# ----------------------- View Files for a Specific Project -----------------------

@views.route('/project/<int:project_id>/files', methods=['GET'])
@login_required
def view_project_files(project_id):
    # Fetch the project
    project = Project.query.get_or_404(project_id)

    # Ensure the current user has access to the project
    if current_user.role == 'contractor' and project.user_id != current_user.id:
        return "Unauthorized", 403
    elif current_user.role == 'subcontractor':
        subcontractor = Subcontractor.query.filter_by(user_id=current_user.id).first()
        if not subcontractor or not Assignment.query.filter_by(project_id=project_id, subcontractor_id=subcontractor.id).first():
            return "Unauthorized", 403

    # Fetch files for the specific project (excluding invoices)
    project_files = File.query.filter_by(project_id=project_id, is_invoice=False).all()

    # Render the project.html template with the project files
    return render_template('project.html', project=project, project_files=project_files, user=current_user)
# ----------------------- invoice view -----------------------

@views.route('/project/invoices')
@login_required
def view_project_invoices():
    user = current_user
    if user.role != 'contractor':
        return "Unauthorized", 403

    assigned_projects = Project.query.filter_by(user_id=user.id).all()
    project_invoices = {}
    new_invoice_count = 0

    for project in assigned_projects:
        invoices = File.query.filter_by(project_id=project.id, is_invoice=True).all()
        project_invoices[project] = invoices
        for invoice in invoices:
            if invoice.is_new:
                new_invoice_count += 1
                invoice.is_new = False  # Mark as viewed
        db.session.commit()

    return render_template(
        'project_invoices.html',
        project_invoices=project_invoices,
        new_invoice_count=new_invoice_count
    )

    return render_template('project_invoices.html', project_invoices=project_invoices)

# ----------------------- Serve Image -----------------------

@views.route('/image/<int:file_id>')
@login_required
def serve_image(file_id):
    file = File.query.get(file_id)
    if not file:
        return "File not found", 404

    # Return the image data with the appropriate MIME type
    return current_app.response_class(file.data, mimetype='image/jpeg')  # Adjust MIME type as needed

# --------------------- Update Task Completion ---------------------

@views.route('/update_task_completion/<int:task_id>', methods=['POST'])
@login_required
def update_task_completion(task_id):
    # Get the task
    task = Task.query.get(task_id)
    if not task:
        flash('Task not found!', category='error')
        return redirect(url_for('views.home'))

    # Get the new completion status from the form
    new_completion_status = request.form.get('completion-status')
    if not new_completion_status:
        flash('Completion status is required!', category='error')
        return redirect(url_for('views.view_project', project_id=task.project_id))

    # Update the task's completion status
    task.completion = new_completion_status
    db.session.commit()
    flash('Task completion status updated successfully!', category='success')
    return redirect(url_for('views.view_project', project_id=task.project_id))