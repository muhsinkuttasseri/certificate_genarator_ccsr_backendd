from schema.doc import *    
from schema.centre import *
from schema.schema import *
from models import *
from flask import jsonify,make_response,request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required



class Centres(MethodResource,Resource):
    @jwt_required(locations=['cookies'])
    @marshal_with(ResponseSchema)
    @use_kwargs(CentreValidatorSchema, location=('json'))
    def post(self,**kwargs):
        try:
            

            centre_dict = Centre(
                name = kwargs.get('name'),
                centre_code = kwargs.get('centre_code')
            )

            db.session.add(centre_dict)
            db.session.commit()
            
            for item in kwargs['course_rel']:
                courses = Course.query.filter_by(id = int(item)).first()
                centre_dict.course_rel.append(courses)  
            db.session.commit()
            

            return make_response(jsonify({'msg': 'success'}),201)

        except SQLAlchemyError as e:
            if 'orig' in e.__dict__.keys():
                print(e.__dict__['orig'].args)
                if e.__dict__['orig'].args[0] == 1062:
                    return make_response(jsonify({'msg': e.__dict__['orig'].args[1]}), 400)
            print(e)
            return make_response(jsonify({'msg': 'Invalid Data'}), 400)

        except Exception as e:
            print(e)
            return make_response(jsonify({'msg': 'Server Error'}), 500)
    
    @jwt_required(locations=['cookies'])
    @marshal_with(CentreResponseSchema)
    def get(self,**kwargs):
        
        try:

            centre_schema = CentreSchema(many=True)
            course_schema = CourseSchema(many=True)
            data = Centre.query.all() 
            print(data)           
            resp = centre_schema.dump(data)
            
            for i in resp:
                courses = db.session.query(Course.course_name,Course.id).filter(Course.id.in_(tuple(i['course_rel']))).all()
                cou_resp = course_schema.dump(courses)
                i['course_rel'] = cou_resp
            print(resp)
            return make_response(jsonify({'msg':'Success','data':resp}),200)
        except Exception as e:
            print(e)
            return make_response(jsonify({'msg':e.args}),500)


class SingleCentre(MethodResource,Resource):

    @jwt_required(locations=['cookies'])
    @marshal_with(CentreResponseSchema)
    def get(self,id,**kwargs):
        
        try:

            centre_schema = CentreSchema(many=True)
            data = Centre.query.filter_by(id=id).all() 
            
            resp = centre_schema.dump(data)[0]
            
            return make_response(jsonify({'msg':'Success','data':resp}),200)
        except Exception as e:
            print(e)
            return make_response(jsonify({'msg':e.args}),500)    

    @jwt_required(locations=['cookies'])
    @marshal_with(ResponseSchema)
    @use_kwargs(CentreValidatorSchema, location=('json'))
    def put(self,id,**kwargs):

        try:
            centres = Centre.query.filter_by(id=id).first()
            
            if centres:
                
                centres.name = kwargs.get('name')
                centres.centre_code = kwargs.get('centre_code')
                db.engine.execute(f"DELETE FROM centre_course WHERE centre_id = {id}")
                for item in kwargs['course_rel']:
                    courses = Course.query.filter_by(id = int(item)).first()
                    centres.course_rel.append(courses) 
                db.session.commit()
                
                return make_response(jsonify({'msg': 'Success'}), 200)
            else:
                return make_response(jsonify({'msg': 'Centre Not Found'}), 400)

        except SQLAlchemyError as e:
            print(e)
            return make_response(jsonify({'msg': 'Invalid Data'}), 400)
        except Exception as e:
            print(e)
            return make_response(jsonify({'msg': 'Server Error'}), 500)