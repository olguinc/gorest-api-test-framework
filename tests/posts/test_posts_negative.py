import pytest

from factories.post_factory import build_post_payload
from utils.assertions import assert_status_code

pytestmark = pytest.mark.negative


def test_create_post_missing_title_returns_422(posts_client, created_user):
    payload = build_post_payload()
    del payload["title"]
    response = posts_client.create_post_for_user(created_user["id"], payload)
    assert_status_code(response, 422)


def test_create_post_for_nonexistent_user_returns_404_or_422(posts_client):
    response = posts_client.create_post_for_user(999_999_999, build_post_payload())
    assert response.status_code in (404, 422)


def test_get_nonexistent_post_returns_404(posts_client):
    response = posts_client.get_post(999_999_999)
    assert_status_code(response, 404)
