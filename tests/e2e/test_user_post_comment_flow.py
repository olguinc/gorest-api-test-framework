import pytest

from factories.comment_factory import build_comment_payload
from factories.post_factory import build_post_payload
from factories.todo_factory import build_todo_payload
from factories.user_factory import build_user_payload
from utils.assertions import assert_status_code

pytestmark = pytest.mark.e2e


def test_user_post_comment_todo_relational_flow(
    users_client, posts_client, comments_client, todos_client, cleanup_registry
):
    # Create the parent user.
    user_response = users_client.create_user(build_user_payload())
    assert_status_code(user_response, 201)
    user = user_response.json()
    cleanup_registry.register("user", user["id"])

    # Create a post owned by that user.
    post_response = posts_client.create_post_for_user(user["id"], build_post_payload())
    assert_status_code(post_response, 201)
    post = post_response.json()
    cleanup_registry.register("post", post["id"])
    assert post["user_id"] == user["id"]

    # Create a comment on that post.
    comment_response = comments_client.create_comment_for_post(post["id"], build_comment_payload())
    assert_status_code(comment_response, 201)
    comment = comment_response.json()
    cleanup_registry.register("comment", comment["id"])
    assert comment["post_id"] == post["id"]

    # Create a todo owned by the same user.
    todo_response = todos_client.create_todo_for_user(user["id"], build_todo_payload())
    assert_status_code(todo_response, 201)
    todo = todo_response.json()
    cleanup_registry.register("todo", todo["id"])
    assert todo["user_id"] == user["id"]

    # Assert the relationships are visible via the nested read endpoints.
    user_posts = users_client.list_posts_for_user(user["id"]).json()
    assert any(p["id"] == post["id"] for p in user_posts)

    post_comments = posts_client.list_comments_for_post(post["id"]).json()
    assert any(c["id"] == comment["id"] for c in post_comments)

    user_todos = users_client.list_todos_for_user(user["id"]).json()
    assert any(t["id"] == todo["id"] for t in user_todos)

    # cleanup_registry fixture deletes comment -> post -> todo -> user on teardown,
    # in that order, so no orphaned child records are left behind.
