# app.py

from flask import Flask
from flask_restx import Api
from test_suite.api1.controllers import api1_ns
from test_suite.api2.controllers import api2_ns

app = Flask(__name__)

# Create the Flask-RESTx API instance
api = Api(app, version='1.0', title='API1', description='API1 documentation', validate=False)

# Add the API1 namespace to the API app
api.add_namespace(api1_ns)
api.add_namespace(api2_ns)

# Custom configuration for Swagger UI
app.config["RESTX_MASK_SWAGGER"] = False  # Disable JSON field masking in Swagger UI
app.config["SWAGGER_UI_REQUEST_DURATION"] = True  # Show request duration in Swagger UI
app.config["SWAGGER_UI_DOC_EXPANSION"] = "none"  # Collapse all sections by default
app.config["VALIDATE_SWAGGER"] = False  # Disable field validation in Swagger UI

if __name__ == '__main__':
    app.run(debug=True)
