from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Lesson

modules_bp = Blueprint('modules', __name__)
modules_api = Api(modules_bp)

class ModuleLessonsAPI(Resource):
    def get(self, module_id):
        lessons = Lesson.query.filter_by(module_id=module_id).order_by(Lesson.order_index).all()
        return[
            {
                "id": l.id,
                "title": l.title,
                "video_url": l.video_url,
                "order_index": l.order_index
            } for l in lessons
        ], 200

    @jwt_required()
    def post(self, module_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'instructor':
            return {"error": "Unauthorized"}, 403

        data = request.get_json()
        new_lesson = Lesson(
            module_id=module_id,
            title=data['title'],
            video_url=data.get('video_url', ''),
            order_index=data.get('order_index', 0)
        )
        db.session.add(new_lesson)
        db.session.commit()
        
        return {"message": "Lesson created", "lesson_id": new_lesson.id}, 201

modules_api.add_resource(ModuleLessonsAPI, '/<string:module_id>/lessons')