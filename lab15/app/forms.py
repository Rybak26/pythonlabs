# app/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, TextAreaField, SelectField, \
    SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, ValidationError
import re
from .models import Tag


class RegistrationForm(FlaskForm):
    username = StringField('Імя користувача', validators=[DataRequired()])
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
    picture = FileField('Оновити зображення профілю', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
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


class TodoForm(FlaskForm):
    title = StringField('Заголовок')
    description = StringField('Опис')
    completed = BooleanField('Завершено')
    submit = SubmitField('Відправити')


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    text = TextAreaField('Текст', validators=[DataRequired()])
    image = FileField('Зображення', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    type = SelectField('Тип', choices=[('News', 'Новина'), ('Publication', 'Публікація'), ('Other', 'Інше')])
    category = SelectField('Категорія', coerce=int)
    tags = SelectMultipleField('Теги', coerce=int)
    submit = SubmitField('Відправити')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
