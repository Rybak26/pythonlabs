# app/main/views.py

import os

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from ..forms import UpdateAccountForm
from ..models import db

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.account'))
    else:
        return redirect(url_for('auth.login'))


@main_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.password.data:
            current_user.password = generate_password_hash(form.password.data)

        current_user.about_me = form.about_me.data

        if form.picture.data:
            _, file_extension = os.path.splitext(form.picture.data.filename)
            new_file_name = secure_filename(f"{current_user.id}.png")
            new_file_path = os.path.join('app/static/profile_images', new_file_name)
            form.picture.data.save(new_file_path)
            current_user.image_file = new_file_name

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    return render_template('account.html', title='Account', form=form)
