from config.config import Api

name = "apiOne"


def setup() -> Api:
    # Create a new instance of _Api
    api_one = Api(name)

    # Setup api_one details
    api_one.app_id = ''
    api_one.base_url.test = ''
    api_one.base_url.beta = ''
    api_one.base_url.prod = ''
    api_one.teams_channel_link = ''

    # Setup auth_zero details for api_one
    api_one.auth_zero.test.audience = '{API_ONE_AUDIENCE}'
    api_one.auth_zero.test.grant_type = '{API_ONE_GRANT_TYPE}'
    api_one.auth_zero.test.client_id = '{API_ONE_CLIENT_ID}'
    api_one.auth_zero.test.client_secret = '{API_ONE_CLIENT_SECRET}'

    api_one.auth_zero.beta.audience = ''
    api_one.auth_zero.beta.grant_type = ''
    api_one.auth_zero.beta.client_id = ''
    api_one.auth_zero.beta.client_secret = ''

    api_one.auth_zero.prod.audience = ''
    api_one.auth_zero.prod.grant_type = ''
    api_one.auth_zero.prod.client_id = ''
    api_one.auth_zero.prod.client_secret = ''

    # Setup controllers_under_test details for api_one
    api_one.controllers_under_test.test = ['', '']
    api_one.controllers_under_test.beta = ['', '']
    api_one.controllers_under_test.prod = ['', '']

    return api_one
