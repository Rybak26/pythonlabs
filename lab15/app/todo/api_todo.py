# app/todo/api_todo.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Todo

api_todo_bp = Blueprint('api_todo', __name__, url_prefix='/api/todos')


@api_todo_bp.route('/todolist', methods=['GET'])
@jwt_required()
def get_todolist():
    current_user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id=current_user_id).all()
    todos_list = [{'id': todo.id, 'title': todo.title, 'description': todo.description, 'completed': todo.completed}
                  for todo in todos]
    return jsonify(todos_list)


@api_todo_bp.route('/addtodo', methods=['POST'])
@jwt_required()
def add_todo():
    current_user_id = get_jwt_identity()
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    title = data.get('title')
    description = data.get('description')
    completed = data.get('completed')
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    todo = Todo(
        user_id=current_user_id,
        title=title,
        description=description,
        completed=completed
    )
    db.session.add(todo)
    db.session.commit()
    return jsonify({'message': 'Todo created successfully'}), 201


@api_todo_bp.route('/edittodo/<int:id>', methods=['PUT'])
@jwt_required()
def edit_todo(id):
    current_user_id = get_jwt_identity()
    todo = Todo.query.get_or_404(id)
    if todo.user_id != current_user_id:
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
@jwt_required()
def delete_todo(id):
    current_user_id = get_jwt_identity()
    todo = Todo.query.get_or_404(id)
    if todo.user_id != current_user_id:
        return jsonify({'error': 'You do not have permission to delete this todo'}), 403

    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'}), 200
