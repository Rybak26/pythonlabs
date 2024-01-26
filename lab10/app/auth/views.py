# app/auth/views.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from ..forms import LoginForm, RegistrationForm
from ..models import User, db
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('User with this username already exists. Please choose a different username.', 'danger')
        else:
            existing_email = User.query.filter_by(email=form.email.data).first()
            if existing_email:
                flash('User with this email already exists. Please use a different email address.', 'danger')
            else:
                if not form.validate_username(form.username):
                    flash('Username can only contain lowercase letters, numbers, and dots.', 'danger')
                else:
                    if not form.validate_email(form.email):
                        flash('Please enter a valid email address.', 'danger')
                    else:
                        hashed_password = generate_password_hash(form.password.data)
                        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
                        db.session.add(new_user)
                        db.session.commit()
                        flash('Registration successful. You can now log in.', 'success')
                        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
