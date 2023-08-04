from config.config import Config, Api


def setup():
    # Create a new instance of _Api
    api_one = Api('apiOne')

    # Setup api_one details
    api_one.app_id = 'app_id_for_apiOne'
    api_one.base_url.test = 'test_url_for_apiOne'
    api_one.base_url.beta = 'beta_url_for_apiOne'
    api_one.base_url.prod = 'prod_url_for_apiOne'
    api_one.teams_channel_link = 'teams_channel_link_for_apiOne'

    # Setup auth_zero details for api_one
    api_one.auth_zero.test.audience = 'test_audience_for_apiOne'
    api_one.auth_zero.test.grant_type = 'test_grant_type_for_apiOne'
    api_one.auth_zero.beta.audience = 'beta_audience_for_apiOne'
    api_one.auth_zero.beta.grant_type = 'beta_grant_type_for_apiOne'
    api_one.auth_zero.prod.audience = 'prod_audience_for_apiOne'
    api_one.auth_zero.prod.grant_type = 'prod_grant_type_for_apiOne'

    # Setup controllers_under_test details for api_one
    api_one.controllers_under_test.test = ['test_controller_1', 'test_controller_2']
    api_one.controllers_under_test.beta = ['beta_controller_1', 'beta_controller_2']
    api_one.controllers_under_test.prod = ['prod_controller_1', 'prod_controller_2']

    # Add api_one to SecretsConfig
    config = Config()
    config.test_apis.add_api(api_one)


setup()
