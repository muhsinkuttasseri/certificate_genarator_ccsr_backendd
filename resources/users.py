import _thread
from schema.doc import *
from flask_restful import Resource,reqparse
from flask import jsonify,make_response
from models import User,db
from schema.schema import *
from utils import *
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import unset_jwt_cookies
import utils
from flask import request
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
import datetime

class Users(MethodResource, Resource):

   @marshal_with(CreateResponseSchema)
   @use_kwargs(UserValidatorSchema, location=('json'))
   @jwt_required(locations=['cookies'])
   def post(self,**kwargs):
      try:
         schema = UserValidatorSchema()
         data = request.get_json(force=True)
         
         errors = schema.validate(data)
         if errors:
            return errors, 422 
         user = schema.load(data)
               
         password  = auto_pass()
         
         password_hash = bcrypt.generate_password_hash(password, 10)
         #  convert yyyy-mm-dd string to python datetime object
         dob = datetime.datetime.strptime(user['dob'], '%Y-%m-%d')
         user['password'] = password_hash
         user['dob']=dob
         user_dict = User(**user)
         db.session.add(user_dict)
         db.session.commit()
         
         _thread.start_new_thread(send_user_email,(user.get('name'),user.get('email'),user.get('email'),password))

         data = {
               "id": user_dict.id
         }
         
         return make_response(jsonify({'msg': 'Success','data': data}), 201)

      except SQLAlchemyError as e:
         print(e.__dict__['orig'].args)
         if e.__dict__['orig'].args[0] == 1062:
               return make_response(jsonify({'msg': e.__dict__['orig'].args[1]}), 400)
         return make_response(jsonify({'msg': e.__dict__['orig'].args}), 400)

      except Exception as e:
         print(e)
         return make_response(jsonify({'msg': 'Server Error'}), 500)
      
   
   # @jwt_required(locations=['cookies'])
   @marshal_with(UserResponseSchema)
   def get(self,**kwargs):
      user_schema = UserSchema(many=True)
      data = (
         db.session.query(
            User.name,User.house,User.mobile,User.email,User.id
         ).all()
      )
      res = user_schema.dump(data)
      return make_response(jsonify({'msg':'Success','data':res}))

class SingleUser(MethodResource,Resource):
   @marshal_with(UserSingleResponseSchema)
   @jwt_required(locations=['cookies'])
   def get(self,id,**kwargs):
      user_schema = UserSchema(many=True)
      data = (
         db.session.query(
            User.name,User.dob,User.house,User.place,User.post,User.mobile,User.email,
            User.pin,User.designation
         ).filter(User.id==id).all()
      )
      res = user_schema.dump(data)[0]
      res['dob'] = res['dob'].replace('T00:00:00','')
      return make_response(jsonify({'msg':'Success','data':res}))

      
   @use_kwargs(UserValidatorSchema, location=('json'))
   @marshal_with(ResponseSchema)
   @jwt_required(locations=['cookies'])
   def put(self,id,**kwargs):
      try:
         schema = UserValidatorSchema()
         data = request.get_json(force=True)
         # print(data)
         errors = schema.validate(data)
         if errors:
            return errors, 422 
         user = schema.load(data)
         # print(user['dob'])
         user_dict = User.query.filter_by(id=id).first()
         if user_dict:
            user_dict.name = user.get('name')
            user_dict.dob = datetime.datetime.strptime(user['dob'], '%Y-%m-%d')

            user_dict.email = user.get('email')
            user_dict.house = user.get('house')
            user_dict.place = user.get('place')
            user_dict.post = user.get('post')
            user_dict.pin = user.get('pin')
            user_dict.mobile = user.get('mobile')
            user_dict.designation = user.get('designation')

               
            db.session.commit()
            return make_response(jsonify({'msg': 'Success'}), 200)
         else:
            return make_response(jsonify({'msg': 'User Not Found'}), 400)

      except SQLAlchemyError as e:
         print(e)
         return make_response(jsonify({'msg': 'Invalid Data'}), 400)
      except Exception as e:
         print(e)
         return make_response(jsonify({'msg': 'Server Error'}), 500)

         
   @marshal_with(ResponseSchema)
   @jwt_required(locations=['cookies'])
   def delete(self,id):
      try:
         user_dict = User.query.filter_by(id=id).first()
         if user_dict:
            db.session.delete(user_dict)
            db.session.commit()
            return make_response(jsonify({'msg': 'Success'}), 200)
         else:
            return make_response(jsonify({'msg': 'User Not Found'}), 400)
      except SQLAlchemyError as e:
         print(e)
         return make_response(jsonify({'msg': 'Invalid Data'}), 400)
      except Exception as e:
         print(e)
         return make_response(jsonify({'msg': 'Server Error'}), 500)
      
class UserLogin(MethodResource,Resource):
   @marshal_with(CreateResponseSchema)
   @use_kwargs(UserLoginValidatorSchema, location=('json'))
   def post(self,**kwargs):
      try:
         
         schema = UserLoginValidatorSchema()
         data = request.get_json(force=True)
         
         errors = schema.validate(data)
         if errors:
            return errors, 422 
         user = schema.load(data)
         
         user_data = User.query.filter(User.email==user.get('email')).first()

         if user_data:

            if bcrypt.check_password_hash(user_data.password,user.get('password')):
               
               #todo
               # genate token
               access_token = create_access_token(identity=user_data.name)
               resp = make_response(jsonify({'msg':'Success','data':{'id':user_data.id}}),200)
               set_access_cookies(resp, access_token)
               return resp
            else:
               return make_response(jsonify({'msg': 'Invalid Username or Password'}), 400)

         return make_response(jsonify({'msg': 'User Not Found'}), 400)

      except SQLAlchemyError as e:
         print(e)
         return make_response(jsonify({'msg': 'Invalid Data'}), 400)
      except Exception as e:
         print(e)
         return make_response(jsonify({'msg': 'Server Error'}), 500)
      
class UserLogout(MethodResource,Resource):
   @marshal_with(ResponseSchema)
   @jwt_required(locations=['cookies'])
   def post(self,**kwargs):
      try:
         resp = make_response(jsonify({'msg':'Success'}),200)
         unset_jwt_cookies(resp)
         return resp


      except SQLAlchemyError as e:
         print(e)
         return make_response(jsonify({'msg': 'Invalid Data'}), 400)
      except Exception as e:
         print(e)
         return make_response(jsonify({'msg': 'Server Error'}), 500)
      
class ForgotPassword(MethodResource,Resource):
   @marshal_with(ResponseSchema)
   @use_kwargs(FPValidatorSchema, location=('json'))
   # OTP send to mail
   def post(self,**kwargs):
      try:
         schema = FPValidatorSchema()
         data = request.get_json(force=True)
   
         errors = schema.validate(data)
         if errors:
            return errors, 422 
         user = schema.load(data)

         user_data = User.query.filter(User.email==user.get('email')).first()
         if user_data:

            # store in cache
            otp = utils.cache_code(user_data.email)
            print(otp)
            
            _thread.start_new_thread(send_otp,(user_data.name,user_data.email,otp))
            return make_response(jsonify({'msg': 'Success'}), 200)
         else:
               return make_response(jsonify({'msg': 'invalid email'}), 400)

      except Exception as e:
         print(e)
         return make_response(jsonify({'msg': 'Server Error'}), 500)

         
   @marshal_with(ResponseSchema)
   @use_kwargs(FPUPDValidatorSchema, location=('json'))
   def put(self,**kwargs):
      # change password
      try:
         schema = FPUPDValidatorSchema()
         data = request.get_json(force=True)
         
         errors = schema.validate(data)
         if errors:
            return errors, 422 
         user = schema.load(data)
         
         otp = utils.code_cache[user['email']]
         print(otp)
    
         if int(otp) == int(user['otp']):
            user_data = User.query.filter(User.email==user.get('email')).first()
            if user_data:
               user_data.password=user.get('password')
               db.session.commit()
               return make_response(jsonify({'msg': 'Success'}), 200)
            else:
               return make_response(jsonify({'msg': 'Invalid Username or Password'}), 400)
         else:
            return make_response(jsonify({'msg': 'invalid otp'}), 400)
      except Exception as e:
         print(e)
         return make_response(jsonify({'msg': 'Server Error'}), 500)