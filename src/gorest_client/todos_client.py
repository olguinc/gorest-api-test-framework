import requests

from gorest_client.base_client import BaseAPIClient


class TodosClient(BaseAPIClient):
    def create_todo_for_user(self, user_id: int, payload: dict) -> requests.Response:
        return self.post(f"/users/{user_id}/todos", json=payload)

    def get_todo(self, todo_id: int) -> requests.Response:
        return self.get(f"/todos/{todo_id}")

    def update_todo(self, todo_id: int, payload: dict) -> requests.Response:
        return self.put(f"/todos/{todo_id}", json=payload)

    def delete_todo(self, todo_id: int) -> requests.Response:
        return self.delete(f"/todos/{todo_id}")
