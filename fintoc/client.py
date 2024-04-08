"""
Module to house the Client object of the Fintoc Python SDK.
"""

from json.decoder import JSONDecodeError

import httpx

from fintoc.paginator import paginate


class Client:
    """Encapsulates the client behaviour and methods."""

    def __init__(self, base_url, api_key, api_version, user_agent, params={}):
        self.base_url = base_url
        self.api_key = api_key
        self.user_agent = user_agent
        self.params = params
        self.__client = None
        self.api_version = api_version

    @property
    def _client(self):
        if self.__client is None:
            self.__client = httpx.Client(
                base_url=self.base_url,
                headers=self.headers,
                params=self.params,
            )
        return self.__client

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
        if paginated:
            return paginate(self._client, path, params=params)
        response = self._client.request(method, path, params=params, json=json)
        response.raise_for_status()
        try:
            return response.json()
        except JSONDecodeError:
            return {}

    def extend(
        self,
        base_url=None,
        api_key=None,
        api_version=None,
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
            api_version=api_version or self.api_version,
            user_agent=user_agent or self.user_agent,
            params={**self.params, **params} if params else self.params,
        )
