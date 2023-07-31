# app.py

from flask import Flask
from test_suite.api1.controllers import api1_ns
from test_suite.api2.controllers import api2_ns
from admin_api import admin_ns
from api import api

app = Flask(__name__)

# Create the Flask-RESTx API instance
api.init_app(app)

# Add the API1 namespace to the API app
api.add_namespace(admin_ns)
api.add_namespace(api1_ns)
# api.add_namespace(api2_ns)

if __name__ == '__main__':
    app.run(debug=True)
