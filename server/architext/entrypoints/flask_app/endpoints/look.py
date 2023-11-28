from flask_jwt_extended import jwt_required, get_jwt_identity
from architext.entrypoints.flask_app.common import ErrorResponseSchema, spec, app, repo
import marshmallow as mm
import architext.service_layer.goodservices as services

class ExitSchema(mm.Schema):
    name = mm.fields.Str(required=True)
    description = mm.fields.Str(required=True)

class RoomSchema(mm.Schema):
    name = mm.fields.Str(required=True)
    description = mm.fields.Str(required=True, default="")

class LookResponseSchema(mm.Schema):
    room = mm.fields.Nested(RoomSchema)
    exits = mm.fields.List(mm.fields.Nested(ExitSchema))

spec.components.schema("LookResponse", schema=LookResponseSchema)

@app.route('/look', methods=['GET'])
@jwt_required()
def look():
    """
    ---
    get:
        description: Look at your current room.
        security:
          - bearerAuth: []
        responses:
            200:
                description: Data for the user.
                content:
                    application/json:
                        schema: LookResponse
            401:
                description: Missing or invalid token.
    """
    user_id = get_jwt_identity()
    try:
        data = services.look(repository=repo, user_id=user_id)
    except Exception as e:
        return ErrorResponseSchema().dump({
            "message": e
        }), 401
    print(data)
    return LookResponseSchema().dump(data)