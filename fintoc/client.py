"""
Module to house the Client object of the Fintoc Python SDK.
"""

import uuid
from json.decoder import JSONDecodeError

import httpx

from fintoc.jws import JWSSignature
from fintoc.paginator import paginate


class Client:
    """Encapsulates the client behaviour and methods."""

    _client = httpx.Client()

    def __init__(
        self,
        base_url,
        api_key,
        api_version,
        user_agent,
        jws_private_key=None,
        params={},
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.user_agent = user_agent
        self.params = params
        self.api_version = api_version
        self.headers = self._get_static_headers()
        self.__jws = JWSSignature(jws_private_key) if jws_private_key else None

    def _get_static_headers(self):
        """Return the headers that do not change per request."""
        headers = {
            "Authorization": self.api_key,
            "User-Agent": self.user_agent,
        }

        if self.api_version is not None:
            headers["Fintoc-Version"] = self.api_version

        return headers

    def _get_headers(self, method, json=None, idempotency_key=None):
        headers = dict(self.headers)
        if self.__jws and json and method.lower() in ["post", "put", "patch"]:
            jws_header = self.__jws.generate_header(json)
            headers["Fintoc-JWS-Signature"] = jws_header

        if method.lower() == "post":
            headers["Idempotency-Key"] = idempotency_key or str(uuid.uuid4())

        return headers

    def request(
        self,
        path,
        paginated=False,
        method="get",
        params=None,
        json=None,
        idempotency_key=None,
    ):
        """
        Uses the internal httpx client to make a simple or paginated request.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        all_params = {**self.params, **params} if params else self.params
        headers = self._get_headers(method, json=json, idempotency_key=idempotency_key)

        if paginated:
            return paginate(self._client, url, headers=headers, params=all_params)

        response = self._client.request(
            method, url, headers=headers, params=all_params, json=json
        )
        response.raise_for_status()
        try:
            return response.json()
        except JSONDecodeError:
            return {}

    def extend(
        self,
        base_url=None,
        api_key=None,
        user_agent=None,
        params=None,
    ):
        """
        Creates a new instance using the data of the current object,
        overwriting parts of it using the method parameters.
        """
        return Client(
            base_url=base_url or self.base_url,
            api_key=api_key or self.api_key,
            api_version=self.api_version,
            user_agent=user_agent or self.user_agent,
            params={**self.params, **params} if params else self.params,
        )
