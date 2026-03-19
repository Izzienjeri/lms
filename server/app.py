import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from models import db
from routes.courses import courses_bp
from routes.auth import auth_bp
from routes.modules import modules_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(courses_bp, url_prefix='/courses')
app.register_blueprint(modules_bp, url_prefix='/modules')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True, port=5000)