from config.config import Api

name = "apiOne"


def setup() -> Api:
    # Create a new instance of _Api
    api_one = Api(name)

    # Setup api_one details
    api_one.app_id = '123'
    api_one.base_url.test = 'http://192.168.1.59/api/'
    api_one.base_url.beta = 'http://fakeurl.beta.com'
    api_one.base_url.prod = 'http://fakeurl.prod.com'
    api_one.teams_channel_link = 'http://faketeamslink.com'

    # Setup controllers_under_test details for api_one
    api_one.controllers_under_test.test = ['', '']
    api_one.controllers_under_test.beta = ['', '']
    api_one.controllers_under_test.prod = ['', '']

    return api_one
