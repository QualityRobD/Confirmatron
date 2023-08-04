class _AuthZeroEnv:
    def __init__(self):
        self.auth_url = ""
        self.audience = ""
        self.grant_type = ""
        self.client_id = ""
        self.client_secret = ""


class _Redis:
    def __init__(self):
        self.redis_host = ""
        self.redis_port = 0


class _ConfirmatronAuthZero:
    def __init__(self):
        self.test = _AuthZeroEnv()
        self.beta = _AuthZeroEnv()
        self.prod = _AuthZeroEnv()


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


class _ApiAuthZero:
    def __init__(self):
        self.test = _AuthZeroEnv()
        self.beta = _AuthZeroEnv()
        self.prod = _AuthZeroEnv()


class Api:
    def __init__(self, api_name: str):
        self.api_name = api_name
        self.app_id = ""
        self.base_url = _BaseUrl()
        self.teams_channel_link = ""
        self.auth_zero = _ApiAuthZero()
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

