import unittest
from modules.json_utility import JsonUtility

class TestJsonUtility(unittest.TestCase):
    def test_to_string(self):
        # Test normal dictionary conversion
        data = {"name": "John", "age": 30}
        result = JsonUtility.serialize(data)
        self.assertEqual(result, '{"name": "John", "age": 30}')

        # Test conversion of a list
        data = [1, 2, 3, 4, 5]
        result = JsonUtility.serialize(data)
        self.assertEqual(result, '[1, 2, 3, 4, 5]')

        # Test conversion of a complex nested dictionary
        data = {"person": {"name": "John", "age": 30}, "scores": [80, 90, 75]}
        result = JsonUtility.serialize(data)
        self.assertEqual(result, '{"person": {"name": "John", "age": 30}, "scores": [80, 90, 75]}')

        # Test conversion of invalid input (should return None)
        data = object()  # Non-serializable object
        result = JsonUtility.serialize(data)
        self.assertIsNone(result)

    def test_from_string(self):
        # Test normal dictionary conversion
        json_str = '{"name": "John", "age": 30}'
        result = JsonUtility.deserialize(json_str)
        self.assertEqual(result, {"name": "John", "age": 30})

        # Test conversion of a list
        json_str = '[1, 2, 3, 4, 5]'
        result = JsonUtility.deserialize(json_str)
        self.assertEqual(result, [1, 2, 3, 4, 5])

        # Test conversion of a complex nested dictionary
        json_str = '{"person": {"name": "John", "age": 30}, "scores": [80, 90, 75]}'
        result = JsonUtility.deserialize(json_str)
        expected_data = {"person": {"name": "John", "age": 30}, "scores": [80, 90, 75]}
        self.assertEqual(result, expected_data)

        # Test conversion of invalid input (should return None)
        json_str = "invalid_json_string"
        result = JsonUtility.deserialize(json_str)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
