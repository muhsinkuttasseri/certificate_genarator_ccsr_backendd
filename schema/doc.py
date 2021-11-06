
from sqlalchemy.orm import relationship
from schema.centre import *
from schema.schema import *
from models import * 
from marshmallow_sqlalchemy import fields
from marshmallow import fields, validate, Schema

class UserGetSchema(Schema):
    name = fields.Str(default='')
    house = fields.Str(default='')
    mobile = fields.Str(default='')
    email = fields.Str(default='')

class UserResponseSchema(Schema):
    message = fields.Str(default='Success')
    data =  fields.Nested(UserGetSchema)

class UserCreateSchema(Schema):
    id = fields.Integer(default=0)
    
class CreateResponseSchema(Schema):
    message = fields.Str(default='Success')
    data =  fields.Nested(UserCreateSchema)
    
class UserSingleResponseSchema(Schema):
    message = fields.Str(default='Success')
    data =  fields.Nested(UserSchema)
    
class CourseResponseSchema(Schema):
    id = fields.Number()
    message = fields.Str(default='Success')
    data =  fields.Nested(CourseSchema)

class SubjectResponseSchema(Schema):
    id = fields.Number()
    message = fields.Str(default='Success')
    data =  fields.Nested(SubjectSchema)    


class CentreResponseSchema(Schema):
    message = fields.Str(default='Success')
    data =  fields.Nested(CentreSchema)

  
class ResponseSchema(Schema):
    message = fields.Str(default='Success')