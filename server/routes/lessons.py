from flask import Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, LessonProgress
from datetime import datetime

lessons_bp = Blueprint('lessons', __name__)
lessons_api = Api(lessons_bp)

class LessonCompleteAPI(Resource):
    @jwt_required()
    def post(self, lesson_id):
        current_user = get_jwt_identity()
        
        progress = LessonProgress.query.filter_by(
            student_id=current_user['id'], 
            lesson_id=lesson_id
        ).first()

        if not progress:
            progress = LessonProgress(
                student_id=current_user['id'],
                lesson_id=lesson_id,
                is_completed=True,
                completed_at=datetime.utcnow()
            )
            db.session.add(progress)
        else:
            progress.is_completed = True
            progress.completed_at = datetime.utcnow()
            
        db.session.commit()
        
        return {"message": "Lesson marked as complete"}, 200

lessons_api.add_resource(LessonCompleteAPI, '/<string:lesson_id>/complete')