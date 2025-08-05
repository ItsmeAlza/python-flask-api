from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app.models import UserModel
from app.schemas.user_schema import UserCreateSchema, UserUpdateSchema, BaseUserSchema
from app.extensions import db
from app.utils.response import success_response, error_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_schema = BaseUserSchema(many=True)
user_create_schema = UserCreateSchema()
user_update_schema = UserUpdateSchema()

class Users(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        pagination = UserModel.query.paginate(page=page, per_page=per_page, error_out=False)
        users = pagination.items

        data = {
            "users": users_schema.dump(users),
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "per_page": pagination.per_page,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        }

        return success_response(data=data)

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return error_response("No input provided", 400)

        try:
            data = user_create_schema.load(json_data)
        except ValidationError as err:
            return error_response(err.messages, 422)

        user = UserModel(
            name=data['name'],
            email=data['email']
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()
        return success_response(data=user_create_schema.dump(user), message="User created", status_code=201)


class User(Resource):
    def get(self, id):
        user = UserModel.query.get(id)
        if not user:
            return error_response("User not found", 404)
        return success_response(data=users_schema.dump(user))

    def patch(self, id):
        user = UserModel.query.get(id)
        if not user:
            return error_response("User not found", 404)

        json_data = request.get_json()
        if not json_data:
            return error_response("No input provided", 400)

        try:
            data = user_update_schema.load(json_data, partial=True)
        except ValidationError as err:
            return error_response(err.messages, 422)

        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']

        db.session.commit()
        return success_response(data=user_update_schema.dump(user), message="User updated")

    def put(self, id):
        user = UserModel.query.get(id)
        if not user:
            return error_response("User not found", 404)

        json_data = request.get_json()
        if not json_data:
            return error_response("No input provided", 400)

        try:
            data = user_update_schema.load(json_data)
        except ValidationError as err:
            return error_response(err.messages, 422)

        user.name = data['name']
        user.email = data['email']

        db.session.commit()
        return success_response(data=user_update_schema.dump(user), message="User replaced")

    def delete(self, id):
        user = UserModel.query.get(id)
        if not user:
            return error_response("User not found", 404)

        db.session.delete(user)
        db.session.commit()
        return success_response(message="User deleted", status_code=204)


class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return error_response("Email and password are required", 400)

        user = UserModel.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return error_response("Invalid email or password", 401)

        access_token = create_access_token(identity=str(user.id))
        return success_response(data={"access_token": access_token}, message="Login successful")
    
class ChangePassword(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = UserModel.query.get(user_id)

        json_data = request.get_json()
        old = json_data.get("old_password")
        new = json_data.get("new_password")
        confirm = json_data.get("confirm_password")

        if not old or not new:
            return error_response("Both old and new passwords are required", 400)
        
        if not confirm:
            return error_response("Confirm password required", 400)
        
        if not user.check_password(old):
            return error_response("Old password is incorrect", 401)
        
        if new != confirm:
            return error_response("New password and confirm password don't match", 400)

        user.set_password(new)
        db.session.commit()
        return success_response(message="Password updated successfully")

