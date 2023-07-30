# controllers.py

from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource, fields
import json

# Create the Namespace
api1_ns = Namespace("api1", description="API1 Namespace")

# Define the model for the request body
address_info_model = api1_ns.model("AddressInfo", {
    "street": fields.String(required=True, description="Street address"),
    "city": fields.String(required=True, description="City"),
    "zip_code": fields.String(required=True, description="Zip code (5 characters)")
})

address_model = api1_ns.model("Address", {
    "type": fields.String(required=True, description="Address type (e.g., home, work)"),
    "info": fields.Nested(address_info_model, required=True)
})

api1_model = api1_ns.model("API1Request", {
    "name": fields.String(required=True, description="Name"),
    "age": fields.Integer(required=True, description="Age"),
    "addresses": fields.List(fields.Nested(address_model), required=True, description="List of addresses")
})


# Create the route for /api1/test
@api1_ns.route("/test", methods=["POST"])
class TestResource(Resource):
    @api1_ns.expect(api1_model)  # Use the expect decorator to specify the expected request body model
    def post(self):
        # Access the request data from the body using the 'json' attribute of the request object
        request_data = request.json

        # Perform any data validation or processing as needed
        # For example, if you expect "name" and "age" fields in the request body:
        name = request_data.get("name")
        age = request_data.get("age")

        # Your logic for processing the data goes here...
        # For example, you could return a dictionary as a JSON-serializable response
        response_data = {"message": f"Received data: Name - {name}, Age - {age}"}

        # Return the JSON-serializable dictionary as a JSON response
        # Convert the response data to JSON using jsonify
        response = jsonify(response_data)

        # If needed, you can also set additional headers for the response
        response.headers["Custom-Header"] = "Custom Value"

        return make_response(response, 201)
