import os
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError

def load_json_schema(file_name: str):
    """Loads a JSON schema from the fixtures/jsonschema folder."""
    schema_path = os.path.normpath(
        os.path.join(
            os.path.dirname(__file__), "..", "fixtures", "jsonschema", file_name
        )
    )

    with open(schema_path, "r", encoding="utf-8") as file:
        return json.load(file)

def validate_json_schema(response_json, schema_source: str):
    """
    Validates a JSON response against a schema.

    - If `schema_source` ends with `.json`, it's treated as a file name in fixtures/jsonschema.
    - Otherwise, it's assumed to be a raw JSON schema string.
    """
    json_schema = (
        load_json_schema(schema_source)
        if schema_source.endswith(".json")
        else json.loads(schema_source)
    )

    try:
        validate(instance=response_json, schema=json_schema)
    except ValidationError as e:
        raise AssertionError(f"❌ JSON schema validation failed: {e.message}")
