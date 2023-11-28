from flask_jwt_extended import jwt_required, get_jwt_identity
from architext.entrypoints.flask_app.common import ErrorResponseSchema, spec, app, repo
import marshmallow as mm
import architext.service_layer.goodservices as services

class UseExitSchema(mm.Schema):
    exit_name = mm.fields.Str(required=True)

class ResponseSchema(mm.Schema):
    message = mm.fields.Str(required=True)

spec.components.schema("UseExit", schema=UseExitSchema)
spec.components.schema("UseExitResponse", schema=ResponseSchema)

@app.route('/use-exit', methods=['POST'])
@jwt_required()
def use_exit():
    """
    ---
    post:
        description: Go through and exit present in the current room
        security:
          - bearerAuth: []
        requestBody:
            required: true
            content:
                application/json:
                    schema: UseExit
        responses:
            200:
                description: Data for the user.
                content:
                    application/json:
                        schema: UseExitResponse
            401:
                description: Missing or invalid token.
    """
    user_id = get_jwt_identity()
    try:
        services.use_exit(exit_name='asdas', repository=repo, user_id=user_id)
    except Exception as e:
        return ErrorResponseSchema().dump({
            "message": e
        }), 401
    return ResponseSchema().dump({ 'message': 'Success' })