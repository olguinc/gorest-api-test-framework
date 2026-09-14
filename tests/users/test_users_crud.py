import pytest

from factories.user_factory import build_user_payload
from utils.assertions import assert_status_code

pytestmark = pytest.mark.crud


def test_create_user(created_user, new_user_payload):
    assert created_user["name"] == new_user_payload["name"]
    assert created_user["email"] == new_user_payload["email"]
    assert "id" in created_user


def test_get_user(users_client, created_user):
    response = users_client.get_user(created_user["id"])
    assert_status_code(response, 200)
    assert response.json()["id"] == created_user["id"]


def test_update_user_put(users_client, created_user):
    updated_payload = build_user_payload(email=created_user["email"])
    response = users_client.update_user(created_user["id"], updated_payload)
    assert_status_code(response, 200)
    assert response.json()["name"] == updated_payload["name"]


def test_update_user_patch(users_client, created_user):
    response = users_client.patch_user(created_user["id"], {"status": "inactive"})
    assert_status_code(response, 200)
    assert response.json()["status"] == "inactive"


def test_delete_user_then_get_returns_404(users_client, cleanup_registry, new_user_payload):
    create_response = users_client.create_user(new_user_payload)
    user_id = create_response.json()["id"]

    delete_response = users_client.delete_user(user_id)
    assert_status_code(delete_response, 204)

    get_response = users_client.get_user(user_id)
    assert_status_code(get_response, 404)
