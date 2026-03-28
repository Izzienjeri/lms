from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Course, Module, Enrollment, LessonProgress, Lesson

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
    def post(self):
        current_user = get_jwt_identity()

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



class CourseEnrollAPI(Resource):
    @jwt_required()
    def post(self, course_id):
        current_user = get_jwt_identity()
        
        course = Course.query.get(course_id)
        if not course:
            return {"error": "Course not found"}, 404

        existing_enrollment = Enrollment.query.filter_by(
            student_id=current_user['id'], 
            course_id=course_id
        ).first()

        if existing_enrollment:
            return {"message": "You are already enrolled in this course"}, 400

        enrollment = Enrollment(student_id=current_user['id'], course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()

        return {"message": "Successfully enrolled in the course"}, 201


class CourseProgressAPI(Resource):
    @jwt_required()
    def get(self, course_id):
        current_user = get_jwt_identity()

        modules = Module.query.filter_by(course_id=course_id).all()
        module_ids = [m.id for m in modules]

        lessons = Lesson.query.filter(Lesson.module_id.in_(module_ids)).all()
        total_lessons = len(lessons)

        if total_lessons == 0:
            return {"progress_percentage": 0, "completed_lessons": 0, "total_lessons": 0}, 200

        lesson_ids = [l.id for l in lessons]
        completed_lessons = LessonProgress.query.filter(
            LessonProgress.student_id == current_user['id'],
            LessonProgress.lesson_id.in_(lesson_ids),
            LessonProgress.is_completed == True
        ).count()

        percentage = (completed_lessons / total_lessons) * 100

        return {
            "progress_percentage": round(percentage, 2),
            "completed_lessons": completed_lessons,
            "total_lessons": total_lessons
        }, 200


courses_api.add_resource(CourseListAPI, '/')
courses_api.add_resource(CourseDetailAPI, '/<string:course_id>')
courses_api.add_resource(CourseModulesAPI, '/<string:course_id>/modules')
courses_api.add_resource(CourseEnrollAPI, '/<string:course_id>/enroll')
courses_api.add_resource(CourseProgressAPI, '/<string:course_id>/progress')
