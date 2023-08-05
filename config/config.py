class AuthZeroEnv:
    def __init__(self, auth_url: str, audience: str, grant_type: str, client_id: str, client_secret: str):
        self.auth_url = auth_url
        self.audience = audience
        self.grant_type = grant_type
        self.client_id = client_id
        self.client_secret = client_secret


class _Redis:
    def __init__(self):
        self.redis_host = ""
        self.redis_port = 0


class _ConfirmatronAuthZero:
    def __init__(self):
        self.test = AuthZeroEnv(
            auth_url="https://dev-qkw5s4olr7o8trqk.us.auth0.com/oauth/token",
            audience="https://dev-qkw5s4olr7o8trqk.us.auth0.com/api/v2/",
            grant_type="client_credentials",
            client_id="WxZ07B3iWSD9r1wbNq0kEZXtS6dX3OTQ",
            client_secret="{CONFIRMATRON_AUTH_ZERO_TEST_CLIENT_SECRET}"
        )
        self.beta = AuthZeroEnv(
            auth_url="{PLACEHOLDER}",
            audience="{PLACEHOLDER}",
            grant_type="{PLACEHOLDER}",
            client_id="{PLACEHOLDER}",
            client_secret="{PLACEHOLDER}"
        )
        self.prod = AuthZeroEnv(
            auth_url="{PLACEHOLDER}",
            audience="{PLACEHOLDER}",
            grant_type="{PLACEHOLDER}",
            client_id="{PLACEHOLDER}",
            client_secret="{PLACEHOLDER}"
        )


class _Confirmatron:
    def __init__(self):
        self.redis = _Redis()
        self.auth_zero = _ConfirmatronAuthZero()


class _BaseUrl:
    def __init__(self):
        self.test = ""
        self.beta = ""
        self.prod = ""


class _ControllersUnderTest:
    def __init__(self):
        self.test = ["", "", "", ""]
        self.beta = ["", "", "", ""]
        self.prod = ["", "", ""]


class Api:
    def __init__(self, api_name: str):
        self.api_name = api_name
        self.app_id = ""
        self.base_url = _BaseUrl()
        self.teams_channel_link = ""
        self.controllers_under_test = _ControllersUnderTest()


class _TestApis:
    def __init__(self):
        self.apis = {}

    def add_api(self, api_name: str, api: Api):
        self.apis[api_name] = api


class Config:
    def __init__(self):
        self.confirmatron = _Confirmatron()
        self.test_apis = _TestApis()

