from marshmallow import Schema, fields, validates, ValidationError

class ReviewSchema(Schema):
    product_id = fields.Int(required=True)
    customer_id = fields.Int(required=True)
    rating = fields.Int(required=True)
    comment = fields.Str(required=False)

    @validates("rating")
    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise ValidationError("Rating must be between 1 and 5.")

    @validates("comment")
    def validate_comment(self, value):
        if len(value) > 500:
            raise ValidationError("Comment must not exceed 500 characters.")
