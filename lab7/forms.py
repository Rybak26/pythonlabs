import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Логін', validators=[DataRequired(), Length(min=4, max=14)])
    email = StringField('Електронна пошта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Підтвердіть пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Реєстрація')

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
