from flask import request, jsonify, make_response, g
from flask_restx import Namespace, Resource
from test_suite.api1.schemas import Api1ModelSchema
from modules.constants import TestStatus
from modules.results import Results
from random import randint

from modules.json_utility import JsonUtility

# Create the Namespace
api1_ns = Namespace("api1", description="API1 Namespace")

# Create instance of TestResult
results = Results()

# Create the route for /api1/test
@api1_ns.route("/test", methods=["POST"])
class TestResource(Resource):
    @api1_ns.expect(Api1ModelSchema())  # Use the expect decorator to specify the expected request body model
    def post(self):

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
            if results.redis_client.exists(g.test_key):
                test_name = f"test-{randint(1,100000000000)}"
                save_data = JsonUtility.to_string(result_data)
                if save_data:
                    test_status = TestStatus.PASS
                else:
                    test_status = TestStatus.FAIL

                results.add_result(g.test_key, test_name, test_status)

            else:
                return make_response(jsonify({
                    'error': f'test-key with value `{g.test_key}` does not exist in our records.'
                }), 400)

        except Exception as e:
            return make_response(jsonify({
                'error': f'Failed to store test results. {e}'
            }), 500)

        return make_response('', 201)
