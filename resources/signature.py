import _thread
from schema.doc import *
from flask_restful import Resource,reqparse
from flask import jsonify,make_response
from models import User,db
from schema.schema import *
from utils import *
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
import utils
from flask import request
from werkzeug.utils import secure_filename
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource

class Signature(MethodResource,Resource):
    @marshal_with(ResponseSchema)
    @jwt_required(locations=['cookies'])
    def post(self,**kwargs):
        try:
            type = request.form['type']

            if 'file' not in request.files:
                return make_response(jsonify({'msg':'No file part'}),400)
            file = request.files['file']
            if file.filename == '':
                return make_response(jsonify({'msg':'No selected file'}),400)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                sign_file = f'http://192.168.1.123:5000/uploads/{filename}'
                
                s_dict = Signatures.query.filter_by(type=type).first()
                if s_dict:
                    print("cvhj")
                    s_dict.signature = sign_file
                    db.session.commit()
                else:
                    print("cvhjzxvcz")
                    sign_dict = Signatures(signature=sign_file,type=type)
                    db.session.add(sign_dict)
                    db.session.commit()

                return make_response(jsonify({'msg':'Success'}),200)
            return make_response(jsonify({'msg':'Invalid file format'}),400)


        except SQLAlchemyError as e:
            print(e)
            return make_response(jsonify({'msg': 'Invalid Data'}), 400)
        except Exception as e:
            print(e)
            return make_response(jsonify({'msg': 'Server Error'}), 500)


    @jwt_required(locations=['cookies'])
    def get(self,**kwargs):
        sign_schema = SignatureSchema(many=True)
        data = (
            db.session.query(
                Signatures.signature,Signatures.type
            ).all()
        )
        res = sign_schema.dump(data)
        return make_response(jsonify({'msg':'Success','data':res}))