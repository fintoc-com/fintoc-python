"""
Module to house the Client object of the Fintoc Python SDK.
"""

import httpx

from fintoc.paginator import paginate


class Client:

    """Encapsulates the client behaviour and methods."""

    def __init__(self, base_url, api_key, user_agent, params={}):
        self.base_url = base_url
        self.api_key = api_key
        self.user_agent = user_agent
        self.params = params
        self.__client = None

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
        return {"Authorization": self.api_key, "User-Agent": self.user_agent}

    def request(self, path, paginated=False, method="get", params=None, json=None):
        """
        Uses the internal httpx client to make a simple or paginated request.
        """
        if paginated:
            return paginate(self._client, path, params=params)
        response = self._client.request(method, path, params=params, json=json)
        response.raise_for_status()
        return response.json()

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
            user_agent=user_agent or self.user_agent,
            params={**self.params, **params} if params else self.params,
        )
