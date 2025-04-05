"""
@File Name: auth.py
@Description: This file contains the authentication routes for user login, logout, and sign-up processes. 
It includes functionality for logging in users, logging out, and creating new user accounts, 
with password hashing for security.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Subcontractor, Assignment, Project
from werkzeug.security import generate_password_hash, check_password_hash # Security
from . import db # Means from __init__.py import database
from flask_login import login_user, login_required, logout_user, current_user # Handles logging in\

auth = Blueprint('auth', __name__)

# --------------------- Login Page ---------------------

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': # Signing in
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # Looking for a specific entry in the database filtered by email
        if user: # Found the user
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if user.role == "subcontractor":
                     subcontractor = Subcontractor.query.filter_by(email=current_user.email).first()
                     assignments = Assignment.query.filter_by(subcontractor_id=subcontractor.id).all() 
                     assigned_projects = db.session.query(Assignment.project_id).filter_by(subcontractor_id=subcontractor.id).all()
                     project_ids = [project[0] for project in assigned_projects]
                     projects = db.session.query(Project).filter(Project.id.in_(project_ids)).all()
                     return render_template("homeSub.html", user=current_user, subcontractor=subcontractor, assignments=assignments, projects=projects)
                else:
                    return redirect(url_for('views.project'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

# --------------------- Logout Function ---------------------

@auth.route('/logout')
@login_required # Decorator, prohibits access to this page/root unless logged in 
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# --------------------- Registry ---------------------

@auth.route('/registry', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST': # Checking Request
        first_name = request.form.get('firstname')
        email = request.form.get('email')
        role = request.form.get('role')
        trade = request.form.get('trade')
        password1 = request.form.get('password')
        password2 = request.form.get('repeat-password')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 3: # Validating (Message Flashing)
            flash('Email must be greater than 2 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Salt length recommended by Chat
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256', salt_length=16), role=role) # pbkdf2:sha256 is a hashing algorithm
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account successfully created!', category='success')
            # Updates Subcontractor Table
            if role == 'subcontractor':
                new_subcontractor = Subcontractor(name=first_name, email=email, trade=trade)
                db.session.add(new_subcontractor)
                db.session.commit()
            return redirect(url_for('views.home')) # Redirect to home page

    return render_template("registry.html", user=current_user)