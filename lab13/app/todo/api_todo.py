# app/todos/api_todo.py

from flask import Blueprint, jsonify, request, redirect, url_for
from flask_login import current_user, login_required
from ..forms import TodoForm
from ..models import db, Todo

api_todo_bp = Blueprint('api_todo', __name__, url_prefix='/api/todos')


@api_todo_bp.route('/todolist', methods=['GET'])
def get_todolist():
    if current_user.is_authenticated:
        todos = Todo.query.filter_by(user_id=current_user.id).all()
        todos_list = [{'id': todo.id, 'title': todo.title, 'description': todo.description, 'completed': todo.completed}
                      for todo in todos]
        return jsonify(todos_list)
    else:
        return jsonify({'error': 'User not authenticated'}), 401


@api_todo_bp.route('/addtodo', methods=['POST'])
def add_todo():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    title = data.get('title')
    description = data.get('description')
    completed = data.get('completed')
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    todo = Todo(
        user_id=current_user.id,
        title=title,
        description=description,
        completed=completed
    )
    db.session.add(todo)
    db.session.commit()
    return jsonify({'message': 'Todo created successfully'}), 201


@api_todo_bp.route('/edittodo/<int:id>', methods=['PUT'])
def edit_todo(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id != current_user.id:
        return jsonify({'error': 'You do not have permission to edit this todo'}), 403

    data = request.json
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.completed = data.get('completed', todo.completed)

    db.session.commit()
    return jsonify({'message': 'Todo edited successfully'}), 200


@api_todo_bp.route('/deletetodo/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id != current_user.id:
        return jsonify({'error': 'You do not have permission to delete this todo'}), 403

    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'}), 200