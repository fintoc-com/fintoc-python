"""
Module to house the Client object of the Fintoc Python SDK.
"""

from json.decoder import JSONDecodeError

import httpx

from fintoc.paginator import paginate


class Client:
    """Encapsulates the client behaviour and methods."""

    _client = httpx.Client()

    def __init__(self, base_url, api_key, api_version, user_agent, params={}):
        self.base_url = base_url
        self.api_key = api_key
        self.user_agent = user_agent
        self.params = params
        self.api_version = api_version

    @property
    def headers(self):
        """Return the appropriate headers for every request."""
        headers = {
            "Authorization": self.api_key,
            "User-Agent": self.user_agent,
        }

        if self.api_version is not None:
            headers["Fintoc-Version"] = self.api_version

        return headers

    def request(self, path, paginated=False, method="get", params=None, json=None):
        """
        Uses the internal httpx client to make a simple or paginated request.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        all_params = {**self.params, **params} if params else self.params
        if paginated:
            return paginate(self._client, url, headers=self.headers, params=all_params)
        response = self._client.request(
            method, url, headers=self.headers, params=all_params, json=json
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
