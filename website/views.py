from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
# organizes!
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) # Main page of website
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # Take in some data from POST request
    # Load it as a Python dictonary of json object
    noteId = note['noteId'] # Access note id attribute
    note = Note.query.get(noteId) # Look for note that has that id
    if note: # If it exists...
        if note.user_id == current_user.id: # if we own that note
            db.session.delete(note) # Delete it
            db.session.commit()
    
    return jsonify({}) # Return empty response