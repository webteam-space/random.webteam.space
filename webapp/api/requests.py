import os
from urllib.parse import urlparse

import requests

import requests_cache
from pybreaker import CircuitBreaker, CircuitBreakerError


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

        self.api_breaker = CircuitBreaker(fail_max=5, reset_timeout=60)

    def request(self, method, url, **kwargs):
        domain = urlparse(url).netloc

        try:
            request = self.api_breaker.call(
                super().request, method=method, url=url, **kwargs
            )
        except requests.exceptions.Timeout:
            raise Exception("The request to {} took too long".format(url))
        except requests.exceptions.ConnectionError:
            raise Exception(
                "Failed to establish connection to {}.".format(url)
            )
        except CircuitBreakerError:
            raise Exception(
                "Requests are closed because of too many failures".format(url)
            )

        return request


class Session(BaseSession, requests.Session):
    pass


class CachedSession(BaseSession, requests_cache.CachedSession):
    def __init__(self, *args, **kwargs):
        # Set cache defaults
        options = {
            "backend": "sqlite",
            "expire_after": 5,
            # Include headers in cache key
            "include_get_headers": True,
        }

        options.update(kwargs)

        super().__init__(*args, **options)
