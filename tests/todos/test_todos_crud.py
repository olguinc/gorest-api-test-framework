import pytest

from utils.assertions import assert_matches_schema, assert_status_code

pytestmark = pytest.mark.crud


def test_create_todo_for_user(created_todo, created_user):
    assert created_todo["user_id"] == created_user["id"]
    assert_matches_schema(created_todo, "todo_schema")


def test_get_todo(todos_client, created_todo):
    response = todos_client.get_todo(created_todo["id"])
    assert_status_code(response, 200)


def test_update_todo_status(todos_client, created_todo):
    response = todos_client.update_todo(
        created_todo["id"],
        {**created_todo, "status": "completed"},
    )
    assert_status_code(response, 200)
    assert response.json()["status"] == "completed"
