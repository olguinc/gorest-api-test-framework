import requests

from gorest_client.base_client import BaseAPIClient


class CommentsClient(BaseAPIClient):
    def create_comment_for_post(self, post_id: int, payload: dict) -> requests.Response:
        return self.post(f"/posts/{post_id}/comments", json=payload)

    def get_comment(self, comment_id: int) -> requests.Response:
        return self.get(f"/comments/{comment_id}")

    def update_comment(self, comment_id: int, payload: dict) -> requests.Response:
        return self.put(f"/comments/{comment_id}", json=payload)

    def delete_comment(self, comment_id: int) -> requests.Response:
        return self.delete(f"/comments/{comment_id}")
