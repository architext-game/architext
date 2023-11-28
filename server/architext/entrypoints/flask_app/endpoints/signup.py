from architext.entrypoints.flask_app.common import ErrorResponseSchema, spec, app, repo
from marshmallow import fields, Schema, ValidationError
from flask import jsonify, request
import architext.service_layer.goodservices as services

class UserSignupSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True)

class UserSignupResponseSchema(Schema):
    message = fields.Str(required=True)
    id = fields.Str(required=True)

spec.components.schema("UserSignup", schema=UserSignupSchema)
spec.components.schema("UserSignupResponse", schema=UserSignupResponseSchema)

@app.route("/signup", methods=['POST'])
def signup_endpoint():
    """
    ---
    post:
        description: Create a new user.
        requestBody:
            required: true
            content:
                application/json:
                    schema: UserSignupSchema
        responses:
            201:
                description: User created successfully.
                content:
                    application/json:
                        schema: UserSignupResponse
            400:
                description: Invalid input.
                content:
                    application/json:
                        schema: ErrorResponse
    """
    try:
        # Deserialize input
        user_data = UserSignupSchema().load(request.json)
        user_id = services.create_user(
            email=user_data['email'],
            name=user_data['name'],
            password=user_data['password'],
            repository=repo
        )

        # Serialize output
        response = UserSignupResponseSchema().dump({
            'message': 'User created successfully',
            'id': user_id
        })
        return jsonify(response), 201

    except ValidationError as err:
        # Handle invalid input
        return jsonify({'message': err.messages}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 400