import json
import os
from jsonschema import Draft202012Validator, ValidationError

class JSONSchemaValidator:
    def __init__(self, schema_dir=None):
        self.schema_dir = schema_dir or os.path.join(os.path.dirname(__file__), "schema")
        self._validators = self._load_all_validators()

    def _load_all_validators(self):
        validators = {}
        for filename in os.listdir(self.schema_dir):
            if filename.endswith(".schema.json"):
                schema_name = filename.replace(".schema.json", "")
                with open(os.path.join(self.schema_dir, filename), "r", encoding="utf-8") as f:
                    schema = json.load(f)
                    validators[schema_name] = Draft202012Validator(schema)
        return validators

    def list_available_schemas(self):
        return list(self._validators.keys())

    def validate(self, data, schema_name):
        if schema_name not in self._validators:
            raise ValueError(f"Schema '{schema_name}' not found in {self.schema_dir}")
        validator = self._validators[schema_name]
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if errors:
            # error_messages = [f"{'/'.join(map(str, err.path))}: {err.message}" for err in errors]
            # raise ValidationError("\n".join(error_messages))
            raise ValidationError("\n".join([f"{'/'.join(map(str, e.path))}: {e.message}" for e in errors]))
        return True
