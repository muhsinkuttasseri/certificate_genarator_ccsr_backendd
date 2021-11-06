import _thread
from schema.doc import *
from flask_restful import Resource,reqparse
from flask import jsonify,make_response
from models import User,db,Course
from schema.schema import *
from utils import *
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
import utils
from flask import request
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource


class Courses(MethodResource,Resource):
    @marshal_with(CreateResponseSchema)
    @use_kwargs(CourseValidatorSchema, location=('json'))
    def post(self,**kwargs):
        try:

            input_list=[]

            schema = CourseValidatorSchema()
            data = request.get_json(force=True)
            print(data)
            subjects = data.get('subject')
            course_id = data.get('course_id')
            
            

            subjects = data.get('subject')

            

            errors = schema.validate(data)
            if errors:
                return errors, 422 

            
                   

            course = schema.load(data)      
            print(course)

            course.pop("subject")
            
            course_dict = Course(**course)
            db.session.add(course_dict)
            db.session.commit()


            db.session.bulk_save_objects(
                    [
                        Subject(
                            course_id = course_dict.id,
                            sub_name = item['sub_name'],
                            type = item['type']
                        )
                        for item in subjects
                    ]
                )
            db.session.commit()


            return make_response(jsonify({'msg': 'Success'}), 201)

        except SQLAlchemyError as e:
            print(e.__dict__['orig'].args)
            if e.__dict__['orig'].args[0] == 1062:
                return make_response(jsonify({'msg': e.__dict__['orig'].args[1]}), 400)
            return make_response(jsonify({'msg': 'Invalid Data'}), 400)

        except Exception as e:
            print(e)
            return make_response(jsonify({'msg': 'Server Error'}), 500) 
    @jwt_required(locations=['cookies'])
    @marshal_with(CourseResponseSchema)
    def get(self):
        course_schema = CourseSchema(many=True)       
        
        data = Course.query.all()
        res = course_schema.dump(data)
        print(res)
        return make_response(jsonify({'msg':'Success','data':res}))

class SingleCourse(MethodResource,Resource):

    @jwt_required(locations=['cookies'])
    @marshal_with(CourseResponseSchema)
    def get(self,id):
        course_schema = CourseSchema(many=True)       
        subject_schema = SubjectSchema(many=True)       
        
        data = Course.query.filter_by(id=id).all()
        res = course_schema.dump(data)[0]
        subs = Subject.query.filter_by(course_id = id).all()
        subsres = subject_schema.dump(subs)
        res['subject'] = subsres
        return make_response(jsonify({'msg':'Success','data':res}))


    @marshal_with(ResponseSchema)
    @use_kwargs(CourseValidatorSchema, location=('json'))
    @jwt_required(locations=['cookies'])
    def put(self,id,**kwargs):
        try:  
              
            subjects=[x for x in kwargs.get('subject') if 'id' in x.keys()]
            newsubs=[x for x in kwargs.get('subject') if 'id' not in x.keys()]
            kwargs.pop('subject')
            
                
            db.session.query(Course).filter(Course.id==id).update(kwargs)
            db.session.bulk_update_mappings(Subject, subjects)
            if newsubs:
                db.session.bulk_save_objects(
                    [
                        Subject(
                            course_id = id,
                            sub_name = item['sub_name'],
                            type = item['type']
                        )
                        for item in subjects
                    ]
                )
            db.session.commit()

            return make_response(jsonify({'msg': 'Success'}), 200)



        except SQLAlchemyError as e:
            print(e)
            return make_response(jsonify({'msg': 'Invalid Data'}), 400)
        except Exception as e:
            print(e)
            return make_response(jsonify({'msg': 'Server Error'}), 500) 
            
    @marshal_with(ResponseSchema)
    # @jwt_required(locations=['cookies'])
    def delete(self,id,**kwargs):
        try:
            course_dict = Course.query.filter_by(id=id).first()
            if course_dict:
                db.session.delete(course_dict)
                db.session.commit()
                return make_response(jsonify({'msg': 'Success'}), 200)
            else:
                return make_response(jsonify({'msg': 'Course Not Found'}), 400)



        except SQLAlchemyError as e:
            print(e)
            return make_response(jsonify({'msg': 'Invalid Data'}), 400)
        except Exception as e:
            print(e)
            return make_response(jsonify({'msg': 'Server Error'}), 500)    

class Subjects(MethodResource,Resource):
    @marshal_with(CreateResponseSchema)
    @use_kwargs(SubjectValidatorSchema, location=('json'))
    def post(self,**kwargs):
        try:
            schema = SubjectValidatorSchema()
            data = request.get_json(force=True)

            errors = schema.validate(data)
            if errors:
                return errors, 422 

            subject = schema.load(data)    

            subject_dict = Subject(**subject)
            db.session.add(subject_dict)
            db.session.commit()

            data = {
                "id": subject_dict.id,
                "course_name" : subject_dict.sub_name,
                "type" : subject_dict.type,
                "course" : subject_dict.course_id
            }
            
            return make_response(jsonify({'msg': 'Success','data': data}), 201)
        except SQLAlchemyError as e:
            print(e.__dict__['orig'].args)
            if e.__dict__['orig'].args[0] == 1062:
                return make_response(jsonify({'msg': e.__dict__['orig'].args[1]}), 400)
            return make_response(jsonify({'msg': 'Invalid Data'}), 400)

        except Exception as e:
            print(e)
            return make_response(jsonify({'msg': 'Server Error'}), 500) 
    # @jwt_required(locations=['cookies'])
    @marshal_with(SubjectResponseSchema)
    def get(self):
        subject_schema = SubjectSchema(many=True)       
        
        data = Subject.query.all()
        res = subject_schema.dump(data)
        print(res)
        return make_response(jsonify({'msg':'Success','data':res}))



class SingleSubject(MethodResource,Resource):
    @marshal_with(ResponseSchema)
    @use_kwargs(SubjectUpdateSchema, location=('json'))
    @jwt_required(locations=['cookies'])
    def put(self,id,**kwargs):
        try:  
            schema = SubjectUpdateSchema()
            data = request.get_json(force=True)
            errors = schema.validate(data)

            if errors:
                return errors, 422 
            subject = schema.load(data)

            if  not subject:
       
                return make_response(jsonify({'msg': 'invalid'}), 400)
                
            subject_dict = Subject.query.filter_by(id=id).update(subject)
            db.session.commit()

            return make_response(jsonify({'msg': 'Success'}), 200)



        except SQLAlchemyError as e:
            print(e)
            return make_response(jsonify({'msg': 'Invalid Data'}), 400)
        except Exception as e:
            print(e)
            return make_response(jsonify({'msg': 'Server Error'}), 500)        


    @marshal_with(ResponseSchema)
    @jwt_required(locations=['cookies'])
    def delete(self,id,**kwargs):
        try:
            subject_dict = Subject.query.filter_by(id=id).first()
            if subject_dict:
                db.session.delete(subject_dict)
                db.session.commit()
                return make_response(jsonify({'msg': 'Success'}), 200)
            else:
                return make_response(jsonify({'msg': 'Subject Not Found'}), 400)

        except SQLAlchemyError as e:
            print(e)
            return make_response(jsonify({'msg': 'Invalid Data'}), 400)
        except Exception as e:
            print(e)
            return make_response(jsonify({'msg': 'Server Error'}), 500)                
