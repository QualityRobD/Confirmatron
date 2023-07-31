from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource
from modules.redis_client import RedisClient
import uuid
from test_suite.api1.models.api1_model import Api1ModelSchema
from modules.JsonUtility import JsonUtility

api_call_results = []

# Create the Namespace
api1_ns = Namespace("api1", description="API1 Namespace")


# Create the route for /api1/test
@api1_ns.route("/test", methods=["POST"])
class TestResource(Resource):
    @api1_ns.expect(Api1ModelSchema)  # Use the expect decorator to specify the expected request body model
    def post(self):

        redis = RedisClient()
        unique_id = str(uuid.uuid4())
        redis_key = f"api1:{unique_id}"

        # Access the validated request data from the body using the 'json' attribute of the request object
        request_data = request.json

        # Perform any data validation or processing as needed
        # You can access the validated fields using the schema
        name = request_data.get("name")
        age = request_data.get("age")

        # Your logic for processing the data goes here...
        # For example, you could return a dictionary as a JSON-serializable response
        result_data = {"message": f"Received data: Name - {name}, Age - {age}"}

        # Return the JSON-serializable dictionary as a JSON response
        # Convert the response data to JSON using jsonify
        try:
            redis.store_result(redis_key, JsonUtility.to_string(result_data))
        except Exception as e:
            print(e)

        response = {"message": "API call successful", "id": unique_id}

        return make_response(jsonify(response), 201)
