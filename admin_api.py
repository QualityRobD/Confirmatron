from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource
from marshmallow_dataclass import dataclass
from modules.redis_client import RedisClient
from modules.json_utility import JsonUtility

# Create the Namespace
admin_ns = Namespace("testAdmin", description="Confirmatron Admin")


# Dataclass for the request payload
@dataclass
class TestKeyPayload:
    api_name: str


# Convert the dataclass into a Marshmallow schema
TestKeyPayloadSchema = TestKeyPayload.Schema()


# Create the route for /api1/test
@admin_ns.route("/createKey", methods=["POST"])
class CreateTestKey(Resource):
    @admin_ns.expect(TestKeyPayloadSchema, validate=True)
    def post(self):
        request_data = admin_ns.payload

        # Deserialize the payload using the Marshmallow schema
        payload_object = TestKeyPayloadSchema.load(request_data)

        # Now you can access the payload attributes like a class
        api_name = payload_object.api_name

        r = RedisClient()
        redis_key = r.create_key(api_name)

        response = {"test_key": f"{redis_key}", "api_name": api_name}

        return make_response(jsonify(response), 201)


@admin_ns.route("/testResults/<string:test_key>", methods=["GET"])
class GetTestResultsByTestKey(Resource):
    def get(self, test_key):
        r = RedisClient()

        results = r.retrieve_results(test_key)

        if not results:
            return make_response(jsonify({
                "error": f"Test Results not found for {test_key}"
            }), 404)

        results = {field: JsonUtility().from_string(data_point) for field, data_point in results.items()}

        # Return the serialized results as a JSON response
        return JsonUtility().from_string(results)

@admin_ns.route("/testKeys", methods=["GET"])
class ListKeysByApiName(Resource):
    def get(self):
        api_name = request.args.get("api_name")
        if not api_name:
            return

        r = RedisClient()

        keys = r.get_redis_keys(api_name)

        # Return the serialized keys as a JSON response
        return make_response(jsonify(keys), 200)
