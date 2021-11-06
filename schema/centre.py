from models import * 
from marshmallow_sqlalchemy import fields
from marshmallow import fields, validate, Schema

class CentreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Centre
        include_relationships = True
        load_instance = True
        # fields = ("id", "name", "centre_code", "course_rel")


class CentreValidatorSchema(Schema):

    name = fields.Str(required=True)
    centre_code = fields.Str(required=True)
    course_rel = fields.List(fields.Int)