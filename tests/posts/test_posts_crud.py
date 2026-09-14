import pytest

from factories.post_factory import build_post_payload
from utils.assertions import assert_matches_schema, assert_status_code

pytestmark = pytest.mark.crud


def test_create_post_for_user(created_post, created_user):
    assert created_post["user_id"] == created_user["id"]
    assert_matches_schema(created_post, "post_schema")


def test_get_post(posts_client, created_post):
    response = posts_client.get_post(created_post["id"])
    assert_status_code(response, 200)


def test_update_post(posts_client, created_post):
    updated_payload = build_post_payload()
    response = posts_client.update_post(created_post["id"], updated_payload)
    assert_status_code(response, 200)
    assert response.json()["title"] == updated_payload["title"]


def test_delete_post_then_get_returns_404(posts_client, created_user):
    create_response = posts_client.create_post_for_user(created_user["id"], build_post_payload())
    post_id = create_response.json()["id"]

    delete_response = posts_client.delete_post(post_id)
    assert_status_code(delete_response, 204)

    get_response = posts_client.get_post(post_id)
    assert_status_code(get_response, 404)
