from typing import Any
import json


class JsonUtility:
    """
    Static class for working with JSON.
    """
    @staticmethod
    def serialize(data: Any) -> str:
        """
        Serialize a Python object into a JSON string.

        :param data: The Python object to be serialized.
        :return: The JSON string.
        :raises ValueError: If the data cannot be serialized into JSON.
        """
        try:
            return json.dumps(data)
        except TypeError as e:
            print(f"Unable to convert {data} to string - {e}")
            raise ValueError(f"Failed to serialize data into JSON: {e}")

    @staticmethod
    def deserialize(json_str: str) -> Any:
        """
        Attempts to deserialize a JSON string into a Python object.

        :param json_str: The JSON string to deserialize.
        :returns: The deserialized Python object.
        :raises json.JSONDecodeError: If the JSON string is invalid.
        """
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # handle or raise the exception as needed
            print(f"Unable to convert {json_str} from string - {e}")
            raise e
