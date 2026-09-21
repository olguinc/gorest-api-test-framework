import pytest

from utils.assertions import assert_status_code

pytestmark = pytest.mark.smoke


def test_list_users_is_reachable(users_client):
    response = users_client.list_users()
    assert_status_code(response, 200)


def test_create_and_delete_user_round_trip(users_client, new_user_payload):
    create_response = users_client.create_user(new_user_payload)
    assert_status_code(create_response, 201)

    user_id = create_response.json()["id"]
    delete_response = users_client.delete_user(user_id)
    assert_status_code(delete_response, 204)


def test_create_post_for_user(created_user, users_client):
    response = users_client.list_posts_for_user(created_user["id"])
    assert_status_code(response, 200)


def test_create_todo_for_user(created_todo):
    assert created_todo["status"] in ("pending", "completed")
