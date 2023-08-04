import json


class JsonUtility:
    @staticmethod
    def to_string(input_value):
        try:
            return json.dumps(input_value)
        except Exception as e:
            print(f"Unable to convert {input_value} to string - {e}")
            return None

    @staticmethod
    def from_string(input_value):
        try:
            return json.loads(input_value)
        except Exception as e:
            print(f"Unable to convert {input_value} from string - {e}")
            return None
