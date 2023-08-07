from flask import g
from functools import wraps
from typing import Callable
from modules.secrets_manager import SecretsManager


def load_api_config(api_name: str) -> Callable:
    """
    A decorator function to load API configuration using a context manager and
    store it in Flask's application context variable (g). The config is available
    during the execution of the decorated route and is cleaned up when the function returns.

    :param api_name: The name of the API whose configuration is to be loaded.
    :returns: Decorator function that can be applied to a Flask route.
    """
    def decorator(func: Callable) -> Callable:
        """
        Decorator function that wraps the original route function, loading the API config before execution.

        :param func: The function to be decorated.
        :returns: The wrapped function.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper function to execute the original function within the context of the loaded API config.

            :param *args: Variable length argument list of the original function.
            :param **kwargs: Arbitrary keyword arguments of the original function.
            :returns: The return value of the original function.
            """
            with SecretsManager.api_context(api_name) as config:
                g.api_config = config.api
                return func(*args, **kwargs)
        return wrapper
    return decorator