import pytest

from factories.user_factory import build_user_payload
from utils.assertions import assert_matches_schema, assert_status_code

pytestmark = pytest.mark.negative


@pytest.mark.parametrize(
    "overrides",
    [
        {"name": ""},
        {"email": "not-an-email"},
        {"gender": "unknown"},
        {"status": "unknown"},
    ],
    ids=["blank-name", "invalid-email", "invalid-gender", "invalid-status"],
)
def test_create_user_invalid_field_returns_422(users_client, overrides):
    response = users_client.create_user(build_user_payload(**overrides))
    assert_status_code(response, 422)
    assert_matches_schema(response.json(), "error_schema")


def test_create_user_missing_email_returns_422(users_client):
    payload = build_user_payload()
    del payload["email"]
    response = users_client.create_user(payload)
    assert_status_code(response, 422)


def test_create_user_duplicate_email_returns_422(users_client, cleanup_registry, created_user):
    duplicate_payload = build_user_payload(email=created_user["email"])
    response = users_client.create_user(duplicate_payload)
    assert_status_code(response, 422)


def test_get_nonexistent_user_returns_404(users_client):
    response = users_client.get_user(999_999_999)
    assert_status_code(response, 404)


def test_request_without_token_returns_401(users_client_no_auth):
    response = users_client_no_auth.list_users()
    assert_status_code(response, 401)
