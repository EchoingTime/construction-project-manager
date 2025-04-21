"""
@File Name: notifications.py
@Description: This file contains the notifications of the Flask application.
"""

from flask import flash
from .models import Message, User, Project, Assignment
from . import db
from datetime import datetime, timedelta

def send_message_notification(sender_id, receiver_id, message_text):
    new_message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        message_text=message_text
    )
    db.session.add(new_message)
    db.session.commit()
    flash('Notification sent to the recipient', category='success')

def send_invoice_notification(subcontractor_id, project_id, filename):
    contractor = User.query.filter_by(role='contractor').first()
    if contractor:
        message_text = f'Invoice uploaded for project {project_id}: {filename}'
        send_message_notification(subcontractor_id, contractor.id, message_text)

def send_deadline_notifications():
    today = datetime.now().date()
    one_week_from_now = today + timedelta(days=7)
    projects = Project.query.filter(Project.deadline.between(today, one_week_from_now)).all()

    for project in projects:
        assignments = Assignment.query.filter_by(project_id=project.id).all()
        for assignment in assignments:
            subcontractor = User.query.get(assignment.subcontractor_id)
            if subcontractor:
                message_text = f'Reminder: Project {project.project_name} deadline is approaching on {project.deadline}'
                send_message_notification(project.user_id, subcontractor.id, message_text)