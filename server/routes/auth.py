from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token
from models import db, User

auth_bp = Blueprint('auth', __name__)

auth_api = Api(auth_bp)

class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()
        
        if User.query.filter_by(email=data['email']).first():
            return {"error": "Email already registered"}, 400
            
        new_user = User(
            name=data['name'],
            email=data['email'],
            role=data.get('role', 'student')
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        return {"message": "User registered successfully"}, 201


class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return {"error": "Invalid email or password"}, 401
            
        access_token = create_access_token(identity={"id": user.id, "role": user.role})
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": {"id": user.id, "name": user.name, "role": user.role}
        }, 200
    
    #

auth_api.add_resource(RegisterAPI, '/register')
auth_api.add_resource(LoginAPI, '/login')