from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from datetime import timedelta

from sqlalchemy.orm import backref


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(weeks=5215)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config.from_object('config.DevelopmentConfig')

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SERVER_NAME'] = "0.0.0.0:5002"

CORS(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Certificate Genaration Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/doc/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/doc-ui/'  # URI to access UI of API Doc
})


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)
jwt = JWTManager(app)
api = Api(app)
docs = FlaskApiSpec(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    mobile = db.Column(db.String(10),nullable=False)
    house = db.Column(db.String(80),nullable=False)
    place = db.Column(db.String(80),nullable=False)
    pin =  db.Column(db.String(6), nullable=False)
    dob = db.Column(db.DateTime())
    post = db.Column(db.String(50),nullable=False)
    designation = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(250))
    
    def __repr__(self):
        return '<User %r>' % self.name
    
class Signatures(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    signature = db.Column(db.String(255))
    # if type is 1 ==> digital signature and 0 ==> signature
    type = db.Column(db.Integer)



centre_course = db.Table('centre_course',
    db.Column('centre_id', db.Integer,db.ForeignKey('centre.id',ondelete='CASCADE'), primary_key=True),
    db.Column('course_id', db.Integer,db.ForeignKey('course.id',ondelete='CASCADE'), primary_key=True)
)

class Centre(db.Model):

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    centre_code = db.Column(db.String(15), nullable=False, unique=True)
    course_rel = db.relationship('Course', secondary=centre_course, backref=db.backref('courses', lazy='dynamic'))


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    course_name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(200), nullable=False)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    sub_name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(200), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id',ondelete='CASCADE'))


    
