from marshmallow import Schema, fields, validate

class CustomerSchema(Schema):
    full_name = fields.String(required=True, validate=validate.Length(min=1))
    username = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=6))
    age = fields.Integer(required=True, validate=validate.Range(min=1))
    address = fields.String(required=True)
    gender = fields.String(validate=validate.OneOf(["Male", "Female", "Other"]))
    marital_status = fields.String(validate=validate.OneOf(["Single", "Married", "Divorced", "Widowed"]))
