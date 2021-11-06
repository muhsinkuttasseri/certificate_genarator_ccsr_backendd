import os
class DevelopmentConfig():
   basedir = os.path.abspath(os.path.dirname(__file__))
   TESTING = True
   UPLOAD_FOLDER = '/uploads'
   # SQLALCHEMY_DATABASE_URI = 'mysql://faris404:12345678@localhost/certificate_generation'
   # SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/certificate_generation'
   # SQLALCHEMY_DATABASE_URI = 'mysql://faris404:12345678@localhost/test1'
   # SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/certificate_generation'
   # SQLALCHEMY_DATABASE_URI = 'mysql://root:2255@localhost/certificate'
   # SQLALCHEMY_DATABASE_URI = 'sqlite://DB/database.db'

   # SQLALCHEMY_DATABASE_URI = 'mysql://root:''@localhost/certificate'
   SQLALCHEMY_DATABASE_URI = f'sqlite:////{basedir}/database.db'
   # sqlite:////tmp/test.db
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   # BASE_URL = 'http://192.168.1.9:5000'
   


class ProductionConfig():
   TESTING = True
   SQLALCHEMY_DATABASE_URI = 'mysql://root:dotdash01@localhost/test2'
   SQLALCHEMY_TRACK_MODIFICATIONS = False
