from architext.entrypoints.flask_app.common import ErrorResponseSchema, spec, app, repo
from marshmallow import fields, Schema, ValidationError
from flask import jsonify, request
import architext.service_layer.goodservices as services
from flask_jwt_extended import create_access_token
import datetime
import architext.entities.exceptions as exceptions

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class UserLoginResponseSchema(Schema):
    username = fields.Str(required=True)
    message = fields.Str(required=True)
    token = fields.Str(required=True)

spec.components.schema("UserLogin", schema=UserLoginSchema)
spec.components.schema("UserLoginReponse", schema=UserLoginResponseSchema)

@app.route('/login', methods=['POST'])
def login():
    """
    ---
    post:
        description: Authenticate a user and provide a JWT token.
        requestBody:
            required: true
            content:
                application/json:
                    schema: UserLogin
        responses:
            200:
                description: Authentication successful.
                content:
                    application/json:
                        schema: UserLoginReponse
            401:
                description: Authentication failed.
                content:
                    application/json:
                        schema: ErrorResponse
    """
    data = UserLoginSchema().load(request.json)

    try:
        user_id = services.login(password=data['password'], username=data['username'], repository=repo)
    except exceptions.UserDoesNotExist:
        return ErrorResponseSchema().dump({
            "message": "Bad username"
        }), 401
    except exceptions.IncorrectPassword:
        return ErrorResponseSchema().dump({
            "message": "Bad password"
        }), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=user_id, expires_delta=datetime.timedelta(days=15))
    return jsonify(access_token=access_token)