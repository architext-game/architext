from marshmallow import Schema, fields
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, request
import architext.service_layer.goodservices as services
from architext.adapters.repository import FakeRepository
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

# Define the Marshmallow schema
class UserSignupSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True)

class UserSignupResponseSchema(Schema):
    message = fields.Str(required=True)
    id = fields.Int(required=True)

class ErrorResponseSchema(Schema):
    message = fields.Str(required=True)

# Create an APISpec
spec = APISpec(
    title="Architext API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# Register schemas with spec
spec.components.schema("UserSignup", schema=UserSignupSchema)
spec.components.schema("UserSignupResponse", schema=UserSignupResponseSchema)
spec.components.schema("ErrorResponse", schema=ErrorResponseSchema)
spec.components.security_scheme("bearerAuth", {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT"
})

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Your App Name"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

repo = FakeRepository()

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
        user_id = services.create_user(
            email=request.json['email'],
            name=request.json['name'],
            password=request.json['password'],
            repository=repo
        )
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    return jsonify({'message': 'User created successfully', 'id': user_id}), 201


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
                    schema:
                        type: object
                        properties:
                            username:
                                type: string
                            password:
                                type: string
        responses:
            200:
                description: Authentication successful.
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                access_token:
                                    type: string
            401:
                description: Authentication failed.
                content:
                    application/json:
                        schema: ErrorResponse
    """
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Validate user here. This is just an example.
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(days=1))
    return jsonify(access_token=access_token)

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    ---
    get:
        description: Access protected data. Requires JWT token.
        security:
          - bearerAuth: []
        responses:
            200:
                description: Data for the user.
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                logged_in_as:
                                    type: string
            401:
                description: Missing or invalid token.
    """
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route("/swagger.json")
def create_swagger_spec():
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                view_func = app.view_functions[rule.endpoint]
                spec.path(view=view_func)
    return jsonify(spec.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
