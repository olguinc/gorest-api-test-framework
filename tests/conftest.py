import pytest

from config.settings import GOREST_BASE_URL, GOREST_TOKEN
from factories.comment_factory import build_comment_payload
from factories.post_factory import build_post_payload
from factories.todo_factory import build_todo_payload
from factories.user_factory import build_user_payload
from gorest_client import CommentsClient, PostsClient, TodosClient, UsersClient
from utils.data_cleanup import CleanupRegistry


@pytest.fixture(scope="session")
def users_client() -> UsersClient:
    return UsersClient(GOREST_BASE_URL, GOREST_TOKEN)


@pytest.fixture(scope="session")
def posts_client() -> PostsClient:
    return PostsClient(GOREST_BASE_URL, GOREST_TOKEN)


@pytest.fixture(scope="session")
def comments_client() -> CommentsClient:
    return CommentsClient(GOREST_BASE_URL, GOREST_TOKEN)


@pytest.fixture(scope="session")
def todos_client() -> TodosClient:
    return TodosClient(GOREST_BASE_URL, GOREST_TOKEN)


@pytest.fixture(scope="session")
def users_client_no_auth() -> UsersClient:
    return UsersClient(GOREST_BASE_URL, "invalid-token")


@pytest.fixture
def cleanup_registry(users_client, posts_client, comments_client, todos_client):
    registry = CleanupRegistry()
    yield registry
    registry.cleanup(
        {
            "comment": comments_client,
            "post": posts_client,
            "todo": todos_client,
            "user": users_client,
        }
    )


@pytest.fixture
def new_user_payload() -> dict:
    return build_user_payload()


@pytest.fixture
def created_user(users_client, cleanup_registry, new_user_payload) -> dict:
    response = users_client.create_user(new_user_payload)
    assert response.status_code == 201, response.text
    user = response.json()
    cleanup_registry.register("user", user["id"])
    return user


@pytest.fixture
def created_post(posts_client, cleanup_registry, created_user) -> dict:
    response = posts_client.create_post_for_user(created_user["id"], build_post_payload())
    assert response.status_code == 201, response.text
    post = response.json()
    cleanup_registry.register("post", post["id"])
    return post


@pytest.fixture
def created_comment(comments_client, cleanup_registry, created_post) -> dict:
    response = comments_client.create_comment_for_post(created_post["id"], build_comment_payload())
    assert response.status_code == 201, response.text
    comment = response.json()
    cleanup_registry.register("comment", comment["id"])
    return comment


@pytest.fixture
def created_todo(todos_client, cleanup_registry, created_user) -> dict:
    response = todos_client.create_todo_for_user(created_user["id"], build_todo_payload())
    assert response.status_code == 201, response.text
    todo = response.json()
    cleanup_registry.register("todo", todo["id"])
    return todo
