from flask import Blueprint, render_template, request, flash, redirect, url_for
from .xml_utils import read_xml, save_xml, add_user_to_xml
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
import xml.etree.ElementTree as ET

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if a user with the given email exists
        user = User.get_by_email(email)
        if user:
            # Verify the password
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # Login the user
                login_user(user, remember=True)
                return redirect(url_for('views.home'))  # Redirect to the home page upon successful login
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Existing code for login and logout routes...

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')

        # Check if user with the same email already exists
        users = read_xml('users.xml')
        for user in users.findall("user"):
            if user.find("email").text == email:
                flash('An account with this email already exists.', category='error')
                return redirect(url_for('auth.signup'))

        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', category='error')
            return redirect(url_for('auth.signup'))

        # Server-side password validation
        if len(password) < 8 or not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not any(char.isdigit() for char in password) or not any(char in "!@#$%^&*" for char in password):
            flash('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.', category='error')
            return redirect(url_for('auth.signup'))

        # Generate hashed password
        hashed_password = generate_password_hash(password)

        # Generate a unique id for the user
        users_tree = ET.parse('users.xml')
        root = users_tree.getroot()
        user_id = len(root.findall('user')) + 1  # Incrementing id

        # Create a new User object
        new_user = User(user_id, email, hashed_password, first_name)

        # Save user data to XML
        new_user.save_to_xml()

        flash('Account created successfully! You can now login.', category='success')
        return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=None)