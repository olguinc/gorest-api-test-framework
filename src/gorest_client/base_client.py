import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from utils.logger import log_request, log_response


class BaseAPIClient:
    """Thin, transparent wrapper around requests.Session.

    Methods return the raw ``requests.Response`` rather than unwrapped JSON so
    callers (tests) can assert on status code, headers, and body independently.
    """

    def __init__(self, base_url: str, token: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=(502, 503, 504),
            allowed_methods=("GET", "POST", "PUT", "PATCH", "DELETE"),
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = self._url(path)
        kwargs.setdefault("timeout", self.timeout)
        log_request(method, url, dict(self.session.headers), **kwargs)

        start = time.monotonic()
        response = self.session.request(method, url, **kwargs)
        elapsed = time.monotonic() - start

        log_response(method, url, response.status_code, elapsed)
        return response

    def get(self, path: str, params: dict | None = None) -> requests.Response:
        return self._request("GET", path, params=params)

    def post(self, path: str, json: dict | None = None) -> requests.Response:
        return self._request("POST", path, json=json)

    def put(self, path: str, json: dict | None = None) -> requests.Response:
        return self._request("PUT", path, json=json)

    def patch(self, path: str, json: dict | None = None) -> requests.Response:
        return self._request("PATCH", path, json=json)

    def delete(self, path: str) -> requests.Response:
        return self._request("DELETE", path)
