import requests

from gorest_client.base_client import BaseAPIClient


class UsersClient(BaseAPIClient):
    def list_users(self, params: dict | None = None) -> requests.Response:
        return self.get("/users", params=params)

    def create_user(self, payload: dict) -> requests.Response:
        return self.post("/users", json=payload)

    def get_user(self, user_id: int) -> requests.Response:
        return self.get(f"/users/{user_id}")

    def update_user(self, user_id: int, payload: dict) -> requests.Response:
        return self.put(f"/users/{user_id}", json=payload)

    def patch_user(self, user_id: int, payload: dict) -> requests.Response:
        return self.patch(f"/users/{user_id}", json=payload)

    def delete_user(self, user_id: int) -> requests.Response:
        return self.delete(f"/users/{user_id}")

    def list_posts_for_user(self, user_id: int) -> requests.Response:
        return self.get(f"/users/{user_id}/posts")

    def list_todos_for_user(self, user_id: int) -> requests.Response:
        return self.get(f"/users/{user_id}/todos")
