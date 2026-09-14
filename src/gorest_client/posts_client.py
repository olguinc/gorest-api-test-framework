import requests

from gorest_client.base_client import BaseAPIClient


class PostsClient(BaseAPIClient):
    def list_posts(self, params: dict | None = None) -> requests.Response:
        return self.get("/posts", params=params)

    def create_post_for_user(self, user_id: int, payload: dict) -> requests.Response:
        return self.post(f"/users/{user_id}/posts", json=payload)

    def get_post(self, post_id: int) -> requests.Response:
        return self.get(f"/posts/{post_id}")

    def update_post(self, post_id: int, payload: dict) -> requests.Response:
        return self.put(f"/posts/{post_id}", json=payload)

    def delete_post(self, post_id: int) -> requests.Response:
        return self.delete(f"/posts/{post_id}")

    def list_comments_for_post(self, post_id: int) -> requests.Response:
        return self.get(f"/posts/{post_id}/comments")
