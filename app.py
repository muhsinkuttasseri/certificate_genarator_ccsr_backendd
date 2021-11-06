from models import app,api,db,User,bcrypt
from flask_jwt_extended import jwt_required
from flask import send_from_directory

from resources.signature import *
from resources.users import *
from resources.course import *
from resources.centre import *


# Protecting static folder/file with jwt
@app.route('/uploads/<path:filename>')
@jwt_required(locations=['cookies'])
def protected(filename):
   return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


api.add_resource(Users,'/api/v1/users')
api.add_resource(SingleUser, '/api/v1/users/<int:id>')
api.add_resource(UserLogin, '/api/v1/login')
api.add_resource(UserLogout, '/api/v1/logout')
api.add_resource(ForgotPassword, '/api/v1/forgot_password')
api.add_resource(Signature , '/api/v1/signature')
api.add_resource(Courses,'/api/v1/course')
api.add_resource(SingleCourse, '/api/v1/course/<int:id>')
api.add_resource(Centres, '/api/v1/centres')
api.add_resource(SingleCentre, '/api/v1/centres/<int:id>')
api.add_resource(Subjects,'/api/v1/subject')
api.add_resource(SingleSubject, '/api/v1/subject/<int:id>')

docs.register(Users)
docs.register(SingleUser)
docs.register(UserLogin)
docs.register(UserLogout)
docs.register(ForgotPassword)
docs.register(Signature)
docs.register(Courses)
docs.register(SingleCourse)
docs.register(Centres)
docs.register(SingleCentre)


if __name__ == '__main__':
   db.create_all()
   if User.query.all() == []:
      print(User.query.all())

      user_data = {
      "name":"admin",
      "email":"admin@gmail.com",
      "mobile":"8111863658",
      "house":"winterfel",
      "place":"winterfel",
      "pin":"673641",
      "dob":datetime.datetime.strptime("2000-02-14", '%Y-%m-%d'),
      "post":"winterfel",
      "designation":"admin",
      "password":bcrypt.generate_password_hash('1234', 10)
      
      }
      user = User(**user_data)
      db.session.add(user)
      db.session.commit()
   app.debug = True
   app.run(host='0.0.0.0',port=5002,debug=True)
