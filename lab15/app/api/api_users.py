# app/api/api_users.py
from flask import Blueprint, jsonify, make_response
from flask_restful import Api, Resource, reqparse, abort
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from ..models import db, User
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

api_users_bp = Blueprint('api_users', __name__, url_prefix='/api/users')
api = Api(api_users_bp)
ma = Marshmallow(api_users_bp)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, help='Username is required', required=True)
parser.add_argument('email', type=str, help='Email is required', required=True)
parser.add_argument('password', type=str, help='Password is required', required=True)


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.jsonify(user)

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        args = parser.parse_args()
        user.username = args['username']
        user.email = args['email']
        user.password = args['password']
        try:
            db.session.commit()
            return user_schema.jsonify(user)
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Failed to update user. Error: {str(e)}")

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Failed to delete user. Error: {str(e)}")


class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.jsonify(users)

    def post(self):
        args = parser.parse_args()

        new_user = User(
            username=args['username'],
            email=args['email'],
            password=args['password']
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            response = user_schema.jsonify(new_user)
            return make_response(response, 201)
        except ValidationError as e:
            db.session.rollback()
            abort(400, message=f"Validation error: {str(e.messages)}")
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Failed to create user. Error: {str(e)}")


api.add_resource(UserResource, '/<int:user_id>')
api.add_resource(UserListResource, '/')