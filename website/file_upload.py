# website/file_upload.py

from flask import Blueprint, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from .models import File, Project
from . import db
from flask_login import login_required

file_upload = Blueprint('file_upload', __name__)

@file_upload.route('/upload-file/<int:project_id>', methods=['POST'])
@login_required
def upload_file(project_id):
    if 'file' not in request.files:
        flash('No file part', category='error')
        return redirect(request.referrer)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file', category='error')
        return redirect(request.referrer)

    if file:
        filename = secure_filename(file.filename)
        new_file = File(filename=filename, data=file.read(), project_id=project_id)
        db.session.add(new_file)
        db.session.commit()
        flash('File successfully uploaded', category='success')
        return redirect(url_for('views.view_project', project_id=project_id))