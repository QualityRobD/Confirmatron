from enum import Enum, auto


class TestStatus(Enum):
    PASS = "pass"
    FAIL = "fail"


class Environments(Enum):
    TEST = auto()
    BETA = auto()
    PROD = auto()

