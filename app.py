# app.py

from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_restx import Api
import os
import importlib.util
from test_suite.api1.controllers import api1_ns
from admin_api import admin_ns


app = Flask(__name__)
CORS(app)

# Create the Flask-RESTx API instance
api = Api(version='1.0', title='Confirmatron', description='API Testing Framework')
api.init_app(app)

test_namespaces = [
    api1_ns,
]


def _call_setup_on_all_api_config_files(directory: str = "config/apis"):
    """
    This function dynamically imports all Python modules in the specified directory and calls a setup function from each one.

    :param directory: The directory that contains the Python modules. Defaults to "config/apis".
    """

    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]  # remove .py extension
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(directory, filename))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.setup()  # call setup function from the module


@app.before_request
def capture_test_key():
    valid_endpoints = []
    for ns in test_namespaces:
        valid_endpoints.extend([resource.resource.endpoint for resource in ns.resources])

    if request.endpoint in valid_endpoints:
        test_key = request.headers.get('test-key')
        if not test_key:
            return jsonify({
                'error': 'test-key is required to be sent in the header'
            }), 400

        # https://flask.palletsprojects.com/en/2.3.x/api/#flask.g
        # g is the expected place in Flask to store stuff for a exactly one request
        g.test_key = request.headers.get('test_key')


# Call the function on application startup
_call_setup_on_all_api_config_files()

# Add the API1 namespace to the API app
api.add_namespace(admin_ns)
for namespace in test_namespaces:
    api.add_namespace(namespace)

if __name__ == '__main__':
    app.run(debug=True)
