# app.py

from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_restx import Api
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


# Add the API1 namespace to the API app
api.add_namespace(admin_ns)
for namespace in test_namespaces:
    api.add_namespace(namespace)

if __name__ == '__main__':
    app.run(debug=True)
