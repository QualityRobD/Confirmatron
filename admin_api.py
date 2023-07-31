from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource
from marshmallow_dataclass import dataclass
from modules.redis_client import RedisClient

# Create the Namespace
admin_ns = Namespace("redis", description="Confirmatron Admin")


# Dataclass for the request payload
@dataclass
class RedisKeyPayload:
    api_name: str


# Convert the dataclass into a Marshmallow schema
RedisKeyPayloadSchema = RedisKeyPayload.Schema()


# Create the route for /api1/test
@admin_ns.route("/createKey", methods=["POST"])
class TestResource(Resource):
    @admin_ns.expect(RedisKeyPayloadSchema, validate=True)
    def post(self):
        request_data = admin_ns.payload

        # Deserialize the payload using the Marshmallow schema
        payload_object = RedisKeyPayloadSchema.load(request_data)

        # Now you can access the payload attributes like a class
        api_name = payload_object.api_name

        r = RedisClient()
        redis_key = r.create_key(api_name)

        response = {"redisKey": f"{redis_key}", "api_name": api_name}

        return make_response(jsonify(response), 201)


@admin_ns.route("/listKeys", methods=["GET"])
class ListKeysResource(Resource):
    def get(self):
        api_name = request.args.get("api_name")

        r = RedisClient()

        keys = r.get_redis_keys(api_name)

        # Return the serialized keys as a JSON response
        return jsonify(keys)
