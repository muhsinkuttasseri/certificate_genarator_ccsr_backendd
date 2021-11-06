from models import * 
from marshmallow_sqlalchemy import fields
from marshmallow import fields, validate, Schema

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        
class SignatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Signatures

class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Course     

class SubjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Subject           

class UserValidatorSchema(Schema):
    name = fields.Str(required=True)
    dob = fields.Str(required=True)
    email = fields.Str(required=True)
    house = fields.Str(required=True)
    place = fields.Str(required=True)
    post = fields.Str(required=True)
    pin = fields.Str(required=True,validate=[validate.Length(min=6, max=6)])
    mobile = fields.Str(required=True,validate=[validate.Length(min=10, max=10)])
    designation = fields.Str(required=True)
    
class UserLoginValidatorSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    
class FPValidatorSchema(Schema):
    email = fields.Str(required=True)
    
class FPUPDValidatorSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    otp = fields.Str(required=True)

class SubjectValidatorSchema(Schema):
    id = fields.Int()
    sub_name = fields.Str(required=True)    
    type = fields.Str(required=True) 

class CourseValidatorSchema(Schema):
    course_name = fields.Str(required=True)    
    type = fields.Str(required=True)   
    subject = fields.List(fields.Nested(SubjectValidatorSchema), required=True) 

# class CourseUpdateSchema(Schema):   
#     course_name = fields.Str()    
#     type = fields.Str() 

class SubjectUpdateSchema(Schema):   
    sub_name = fields.Str()    
    type = fields.Str()     







