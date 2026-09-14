import pytest

from factories.comment_factory import build_comment_payload
from utils.assertions import assert_matches_schema, assert_status_code

pytestmark = pytest.mark.crud


def test_create_comment_for_post(created_comment, created_post):
    assert created_comment["post_id"] == created_post["id"]
    assert_matches_schema(created_comment, "comment_schema")


def test_get_comment(comments_client, created_comment):
    response = comments_client.get_comment(created_comment["id"])
    assert_status_code(response, 200)


def test_delete_comment_then_get_returns_404(comments_client, created_post):
    create_response = comments_client.create_comment_for_post(
        created_post["id"], build_comment_payload()
    )
    comment_id = create_response.json()["id"]

    delete_response = comments_client.delete_comment(comment_id)
    assert_status_code(delete_response, 204)

    get_response = comments_client.get_comment(comment_id)
    assert_status_code(get_response, 404)
