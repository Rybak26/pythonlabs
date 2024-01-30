# app/posts/views.py
import datetime
import os

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from ..forms import PostForm
from ..models import db, Post, Category, Tag

posts_bp = Blueprint('posts', __name__)


@posts_bp.route('/posts', methods=['GET'])
def posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(desc(Post.created)).paginate(page=page, per_page=5, error_out=False)
    return render_template('posts/posts.html', posts=posts)


@posts_bp.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    categories = Category.query.all()
    form.category.choices = [(category.id, category.name) for category in categories]

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            text=form.text.data,
            user_id=current_user.id,
            category_id=form.category.data,
            type=form.type.data
        )

        tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        post.tags.extend(tags)

        db.session.add(post)
        db.session.commit()

        if form.image.data:
            new_file_name = f"{post.id}.png"
            file_path = os.path.join('app/static/post_images', new_file_name)
            form.image.data.save(file_path)
            post.image = new_file_name

        db.session.commit()

        flash('Post created successfully!', 'success')
        return redirect(url_for('posts.posts'))

    return render_template('posts/add_post.html', form=form)


@posts_bp.route('/my_posts', methods=['GET'])
@login_required
def my_posts():
    page = request.args.get('page', 1, type=int)
    user_posts = Post.query.filter_by(user_id=current_user.id).order_by(desc(Post.created)).paginate(page=page, per_page=5, error_out=False)
    form = PostForm()
    return render_template('posts/my_posts.html', user_posts=user_posts, form=form)


@posts_bp.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]

    post_tags = [tag.id for tag in post.tags]

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.type = form.type.data
        post.category_id = form.category.data
        post.created = datetime.datetime.utcnow()

        tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        post.tags = tags

        if form.image.data:
            _, file_extension = os.path.splitext(form.image.data.filename)
            new_file_name = secure_filename(f"{post.id}.png")
            new_file_path = os.path.join('app/static/post_images', new_file_name)
            form.image.data.save(new_file_path)
            post.image = new_file_name

        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('posts.my_posts'))

    return render_template('posts/edit_posts.html', form=form, post=post)


@posts_bp.route('/delete_post/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if current_user.id != post.user_id:
        flash('You do not have permission to delete this post.', 'danger')
        return redirect(url_for('posts.my_posts'))

    db.session.delete(post)
    db.session.commit()

    flash('Post deleted successfully!', 'success')
    return redirect(url_for('posts.my_posts'))
