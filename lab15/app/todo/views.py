# app/todos/views.py

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from ..forms import TodoForm
from ..models import db, Todo

todos_bp = Blueprint('todos', __name__)


@todos_bp.route('/todolist')
def todolist():
    if current_user.is_authenticated:
        todos = Todo.query.filter_by(user_id=current_user.id).all()
        return render_template('todos/index.html', todos=todos)
    else:
        return redirect(url_for('auth.login'))


@todos_bp.route('/addtodo', methods=['GET', 'POST'])
def add_todo():
    form = TodoForm()
    if form.validate_on_submit():
        todo = Todo(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            completed=form.completed.data
        )
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todos.todolist'))
    return render_template('todos/add_todo.html', form=form)


@todos_bp.route('/edittodo/<int:id>', methods=['GET', 'POST'])
def edit_todo(id):
    todo = Todo.query.get_or_404(id)
    form = TodoForm(obj=todo)
    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        todo.completed = form.completed.data
        db.session.commit()
        return redirect(url_for('todos.todolist'))
    return render_template('todos/edit_todo.html', form=form, todo=todo)


@todos_bp.route('/deletetodo/<int:id>')
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todos.todolist'))
