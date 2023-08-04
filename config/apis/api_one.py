from config.config import Config, Api


def setup():
    # Create a new instance of _Api
    api_one = Api('apiOne')

    # Setup api_one details
    api_one.app_id = ''
    api_one.base_url.test = ''
    api_one.base_url.beta = ''
    api_one.base_url.prod = ''
    api_one.teams_channel_link = ''

    # Setup auth_zero details for api_one
    api_one.auth_zero.test.audience = ''
    api_one.auth_zero.test.grant_type = ''
    api_one.auth_zero.test.client_id = ''
    api_one.auth_zero.test.client_secret = ''

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

    # Add api_one to SecretsConfig
    config = Config()
    config.test_apis.add_api(api_one)


setup()
