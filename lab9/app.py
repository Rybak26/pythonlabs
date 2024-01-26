import os
import re
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Email, ValidationError, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nedavaytepovtorkyplease'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///povtorka.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_default_image_filename(self):
        return f'default_{self.id}.jpg'


class RegistrationForm(FlaskForm):
    username = StringField('Ім\'я користувача', validators=[DataRequired()])
    email = StringField('Електронна пошта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зареєструватися')

    def validate_email(self, email):
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not email_pattern.match(email.data):
            return False
        return True

    def validate_username(self, username):
        username_pattern = re.compile(r'^[a-z0-9.]+$')
        if not username_pattern.match(username.data):
            return False
        return True


class LoginForm(FlaskForm):
    email = StringField('Електронна пошта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запамятати мене')
    submit = SubmitField('Увійти')


class UpdateAccountForm(FlaskForm):
    username = StringField('Імя користувача', validators=[DataRequired()])
    email = StringField('Електронна пошта', validators=[DataRequired(), Email()])
    submit = SubmitField('Оновити')
    picture = FileField('Оновити фото профілю', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    about_me = StringField('Про мене', validators=[Length(min=0, max=140)])
    password = PasswordField('Новий пароль')

    def validate_email(self, email):
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not email_pattern.match(email.data):
            return False
        return True

    def validate_username(self, username):
        username_pattern = re.compile(r'^[a-z0-9.]+$')
        if not username_pattern.match(username.data):
            return False
        return True


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Користувач з таким ім\'ям користувача вже існує. Будь ласка, виберіть інше ім\'я користувача.', 'danger')
        else:
            existing_email = User.query.filter_by(email=form.email.data).first()
            if existing_email:
                flash('Користувач з такою електронною адресою вже існує. Будь ласка, використовуйте іншу електронну адресу.', 'danger')
            else:
                if not form.validate_username(form.username):
                    flash('Ім\'я користувача може містити тільки строчні літери, цифри та крапки.', 'danger')
                else:
                    if not form.validate_email(form.email):
                        flash('Будь ласка, введіть дійсну електронну адресу.', 'danger')
                    else:
                        hashed_password = generate_password_hash(form.password.data)
                        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
                        db.session.add(new_user)
                        db.session.commit()
                        flash('Реєстрація успішна. Тепер ви можете увійти.', 'success')
                        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Невдала спроба входу. Будь ласка, перевірте електронну адресу та пароль.', 'danger')
    return render_template('login.html', title='Вхід', form=form)


@app.route('/account', methods=['GET', 'POST'])
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
            new_file_name = secure_filename(f"{current_user.id}{file_extension}")
            new_file_path = os.path.join('static/profile_images', new_file_name)
            form.picture.data.save(new_file_path)
            current_user.image_file = new_file_name

        db.session.commit()
        flash('Ваш обліковий запис був оновлений!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    return render_template('account.html', title='Обліковий запис', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
