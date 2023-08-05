from config.config import Api

name = "apiOne"


def setup() -> Api:
    # Create a new instance of _Api
    api_one = Api(name)

    # Setup api_one details
    api_one.app_id = ''
    api_one.base_url.test = 'http://192.168.1.59/api/'
    api_one.base_url.beta = ''
    api_one.base_url.prod = ''
    api_one.teams_channel_link = ''

    # Setup controllers_under_test details for api_one
    api_one.controllers_under_test.test = ['', '']
    api_one.controllers_under_test.beta = ['', '']
    api_one.controllers_under_test.prod = ['', '']

    return api_one
