from flask_jwt_extended import jwt_required, get_jwt_identity
from architext.entrypoints.flask_app.common import ErrorResponseSchema, spec, app, repo
import marshmallow as mm
import architext.service_layer.goodservices as services
from flask import jsonify, request


class CreateConnectedRoomSchema(mm.Schema):
    room_name: mm.fields.Str(required=True)
    room_description: mm.fields.Str(required=True)
    entrance_name: mm.fields.Str(required=True)
    exit_name: mm.fields.Str(required=True)

class ResponseSchema(mm.Schema):
    message = mm.fields.Str(required=True)

spec.components.schema("CreateConnectedRoom", schema=CreateConnectedRoomSchema)
spec.components.schema("CreateConnectedRoomResponse", schema=ResponseSchema)

@app.route('/create-connected-room', methods=['POST'])
@jwt_required()
def create_connected_room():
    """
    ---
    post:
        description: Create a room connected to the current room
        security:
          - bearerAuth: []
        requestBody:
            required: true
            content:
                application/json:
                    schema: CreateConnectedRoom
        responses:
            200:
                description: Success.
                content:
                    application/json:
                        schema: CreateConnectedRoomResponse
            401:
                description: Missing or invalid token.
    """
    user_id = get_jwt_identity()
    data = CreateConnectedRoomSchema().load(request.json)
    try:
        room_id = services.create_connected_room(
            repository=repo,
            user_id=user_id,
            name=data['room_name'],
            description=data['room_description'],
            entrance_name=data['entrance_name'],
            exit_name=data['exit_name']
        )
    except Exception as e:
        return ErrorResponseSchema().dump({
            "message": e
        }), 401
    return ResponseSchema().dump({ 'message': 'Success' })