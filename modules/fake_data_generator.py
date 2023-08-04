import prance
from faker import Faker
import json

fake = Faker()

# Define a function that generates fake data based on schema types
def generate_fake_data(schema):
    if 'type' not in schema:
        return None

    if schema['type'] == 'string':
        return fake.pystr_format()

    if schema['type'] == 'integer':
        return fake.pyint()

    if schema['type'] == 'number':
        return fake.pyfloat()

    if schema['type'] == 'boolean':
        return fake.pybool()

    if schema['type'] == 'array':
        item_schema = schema.get('items', {})
        return [generate_fake_data(item_schema) for _ in range(fake.pyint(min_value=1, max_value=5))]

    if schema['type'] == 'object':
        properties = schema.get('properties', {})
        required = schema.get('required', [])
        obj = {}
        for prop, prop_schema in properties.items():
            obj[prop] = generate_fake_data(prop_schema)
        for req in required:
            if req not in obj:
                obj[req] = generate_fake_data(properties.get(req, {}))
        return obj

    return None

# Parse the OpenAPI spec and generate a sample payload for each endpoint
def print_sample_payloads(spec_url):
    parser = prance.ResolvingParser(spec_url)
    for path, path_obj in parser.specification['paths'].items():
        for method, method_obj in path_obj.items():
            if 'requestBody' in method_obj:
                content = method_obj['requestBody'].get('content', {})
                if 'application/json' in content:
                    schema = content['application/json'].get('schema', {})
                    print(f"Endpoint: {method.upper()} {path}")
                    print("Sample Payload:")
                    payload = generate_fake_data(schema)
                    print(json.dumps(payload, indent=4, sort_keys=True))
                    print()

print_sample_payloads('https://petstore3.swagger.io/api/v3/openapi.json')
