# app/models.py

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

post_tags = db.Table('post_tags', db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True), db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True))


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


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    completed = db.Column(db.Boolean, default=False)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    type = db.Column(db.Enum('News', 'Publication', 'Other'), nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    category = db.relationship('Category', backref='posts')
    tags = db.relationship('Tag', secondary=post_tags, backref='posts')

    def __repr__(self):
        return f'<Post {self.title}>'

    def get_user(self):
        return User.query.get(self.user_id)


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<Category {self.name}>'


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<Tag {self.name}>'
