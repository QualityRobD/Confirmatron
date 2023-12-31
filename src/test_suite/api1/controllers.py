from flask import request, jsonify, make_response, g
from flask_restx import Namespace, Resource
from random import randint
from test_suite.api1.schemas import Api1ModelSchema
from modules.constants import TestStatus
from modules.results import Results
from modules.json_utility import JsonUtility
from modules.http_client import HttpClient
from modules.constants import Environments
from modules.decorators import load_api_config

# Create the Namespace
api1_ns = Namespace("api1", description="API1 Namespace")

# Create instance of TestResult
results = Results()


@api1_ns.route("/test", methods=["POST"])
class TestResource(Resource):
    @api1_ns.expect(Api1ModelSchema())  # Use the expect decorator to specify the expected request body model
    @load_api_config("apiOne")
    def post(self):
        http_client = HttpClient("http://192.168.1.59/api/", Environments.TEST)

        api_name = g.api_config.api_name
        app_id = g.api_config.app_id
        base_url_test = g.api_config.base_url.test
        base_url_beta = g.api_config.base_url.beta
        base_url_prod = g.api_config.base_url.prod
        teams_channel_link = g.api_config.teams_channel_link
        controllers_under_test = g.api_config.controllers_under_test

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
        response = http_client.get("private")
        response.raise_for_status()

        try:

            if results.redis_client.exists(g.test_key):
                test_name = f"test-{randint(1, 100000000000)}"
                save_data = JsonUtility.serialize(result_data)
                if save_data:
                    test_status = TestStatus.PASS
                else:
                    test_status = TestStatus.FAIL

                results.add_result(g.test_key, test_name, test_status, payload_sent={}, payload_received={}, context="")

            else:
                return make_response(jsonify({
                    'error': f'test-key with value `{g.test_key}` does not exist in our records.'
                }), 400)

        except Exception as e:
            return make_response(jsonify({
                'error': f'Failed to store test results. {e}'
            }), 500)

        return make_response('', 201)
