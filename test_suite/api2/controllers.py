# test_suite/api2/controllers.py

from flask_restx import Namespace, Resource

# Create the Namespace object for API1
api2_ns = Namespace('API2', description='API2 endpoints')

# Endpoint for /api1/test
@api2_ns.route('/test')
class TestResource(Resource):
    @api2_ns.doc(description='Get test data')
    def get(self):
        # Define the functionality of the /api1/test GET endpoint here
        return {'message': 'This is the /api2/test endpoint in API1'}

    @api2_ns.doc(description='Post test data')
    def post(self):
        # Define the functionality of the /api1/test POST endpoint here
        return {'message': 'This is the /api2/test endpoint in API1'}
