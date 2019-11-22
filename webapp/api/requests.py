import os
from urllib.parse import urlparse

import requests

import requests_cache


class TimeoutHTTPAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, timeout=None, *args, **kwargs):
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, *args, **kwargs):
        kwargs["timeout"] = self.timeout
        return super().send(*args, **kwargs)


class BaseSession:
    """A base session interface to implement common functionality

    Create an interface to manage exceptions and return API exceptions
    """

    def __init__(self, timeout=(0.5, 3), *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mount("http://", TimeoutHTTPAdapter(timeout=timeout))
        self.mount("https://", TimeoutHTTPAdapter(timeout=timeout))

    def request(self, method, url, **kwargs):
        domain = urlparse(url).netloc

        try:
            request = super().request(method=method, url=url, **kwargs)
        except requests.exceptions.Timeout:
            raise Exception("The request to {} took too long".format(url))
        except requests.exceptions.ConnectionError:
            raise Exception(
                "Failed to establish connection to {}.".format(url)
            )

        return request


class Session(BaseSession, requests.Session):
    pass


class CachedSession(BaseSession, requests_cache.CachedSession):
    def __init__(self, *args, **kwargs):
        # Set cache defaults
        options = {
            "expire_after": 5,
            # Include headers in cache key
            "include_get_headers": True,
        }

        options.update(kwargs)

        super().__init__(*args, **options)
