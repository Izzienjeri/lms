import json

from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Course, Module

courses_bp = Blueprint('courses', __name__)
courses_api = Api(courses_bp)

class CourseListAPI(Resource):
    def get(self): 
        courses = Course.query.filter_by(is_published=True).all()
        return[
            {
                "id": c.id,
                "title": c.title,
                "description": c.description,
                "instructor_id": c.instructor_id
            } for c in courses
        ], 200
    
    @jwt_required()
    def put(self):

        if request.method != 'PUT':
            return {"error": "Method not allowed"}, 405

        data = request.get_json()

        course = Course.query.get(data['id'])
        if not course:
            return {"error": "Course not found"}, 404
        
        course.title = data.get('title', course.title)
        course.description = data.get('description', course.description)
        course.is_published = data.get('is_published', course.is_published)
        
        db.session.commit()

        return {"message": "Course updated successfully"}, 200

    @jwt_required()
    def post(self):
        current_user = json.loads(get_jwt_identity())

        if current_user['role'] != 'instructor':
            return {"error": "Only instructors can create courses!!!"}, 403
        
        data = request.get_json()
        new_course = Course (
            title=data['title'],
            description=data.get('description', ''),
            instructor_id=current_user['id'],
            is_published=data.get('is_published', False)
        )

        db.session.add(new_course)
        db.session.commit()

        return {"message": "Course created successfully", "course_id": new_course.id}, 201


class CourseDetailAPI(Resource):
    def get(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            return {"error": "course not found"}, 404
        
        return {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "instructor_id": course.instructor_id,
            "is_published": course.is_published
        }, 200
    

class CourseModulesAPI(Resource):
    def get(self, course_id):
        modules = Module.query.filter_by(course_id=course_id).order_by(Module.order_index).all()
        return[
            {
                "id": m.id,
                "title": m.title,
                "order_index": m.order_index
            } for m in modules
        ], 200

    @jwt_required()
    def post(self, course_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'instructor':
            return {"error": "Unauthorized"}, 403

        data = request.get_json()
        new_module = Module(
            course_id=course_id,
            title=data['title'],
            order_index=data.get('order_index', 0)
        )
        db.session.add(new_module)
        db.session.commit()
        
        return {"message": "Module created", "module_id": new_module.id}, 201


courses_api.add_resource(CourseListAPI, '/')
courses_api.add_resource(CourseDetailAPI, '/<string:course_id>')
courses_api.add_resource(CourseModulesAPI, '/<string:course_id>/modules')