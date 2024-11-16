from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/login', methods=['GET', "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')
        pass_hash = get_password(email)
        if check_password_hash(pass_hash, password):
            flash('Logged In!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash("Email or Password does not match an existing user", category='error')
    return render_template("login.html", text="Testing")

@views.route('/create_account')
def create_account():
    pass
"""
    if request.method == 'POST':
        if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')"""
        