import pytest

from utils.assertions import assert_matches_schema, assert_response_time_under

pytestmark = pytest.mark.schema


def test_single_user_matches_schema(created_user, users_client):
    response = users_client.get_user(created_user["id"])
    assert_matches_schema(response.json(), "user_schema")
    assert_response_time_under(response)


def test_user_list_matches_schema(users_client):
    response = users_client.list_users(params={"per_page": 5})
    assert_matches_schema(response.json(), "user_schema")
    assert_response_time_under(response)
