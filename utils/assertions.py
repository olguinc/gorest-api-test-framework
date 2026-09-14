import json
from pathlib import Path

import jsonschema
import requests

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"


def assert_status_code(response: requests.Response, expected: int) -> None:
    assert response.status_code == expected, (
        f"Expected status {expected}, got {response.status_code}. Body: {response.text}"
    )


def assert_matches_schema(payload: dict | list, schema_name: str) -> None:
    schema_path = SCHEMAS_DIR / f"{schema_name}.json"
    schema = json.loads(schema_path.read_text())

    if isinstance(payload, list) and schema.get("type") != "array":
        schema = {"type": "array", "items": schema}

    jsonschema.validate(instance=payload, schema=schema)


def assert_response_time_under(response: requests.Response, seconds: float = 3.0) -> None:
    elapsed = response.elapsed.total_seconds()
    assert elapsed < seconds, f"Response took {elapsed:.2f}s, expected under {seconds}s"
