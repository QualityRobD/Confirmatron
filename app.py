# app.py

from flask import Flask
from flask_restx import Api
from test_suite.api1.controllers import api1_ns
from test_suite.api2.controllers import api2_ns

app = Flask(__name__)

# Create the Flask-RESTx API instance
api = Api(app, version='1.0', title='Confirmatron', description='API Testing Framework')

# Add the API1 namespace to the API app
api.add_namespace(api1_ns)
api.add_namespace(api2_ns)

if __name__ == '__main__':
    app.run(debug=True)
