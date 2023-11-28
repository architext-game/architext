from marshmallow import Schema, fields
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, request

from architext.adapters.repository import FakeRepository
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager

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

@app.route("/swagger.json")
def create_swagger_spec():
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                view_func = app.view_functions[rule.endpoint]
                spec.path(view=view_func)
    return jsonify(spec.to_dict())
