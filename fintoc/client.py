"""
client.py
=========

The client to make requests to the Fintoc API.
"""

from functools import reduce
from importlib import import_module
from operator import itemgetter
import re
import httpx

from fintoc import __version__
from fintoc.resources import Link
from fintoc.utils import fieldsubs, pick, rename_keys, snake_to_pascal

SCHEME = "https://"
BASE_URL = "api.fintoc.com/v1/"


class Client:
    def __init__(self, api_key):
        self.api_key = api_key
        self.user_agent = f"fintoc-python/{__version__}"

        self.headers = {"Authorization": self.api_key, "User-Agent": self.user_agent}
        self._client = httpx.Client(base_url=SCHEME + BASE_URL, headers=self.headers)

        self.get = self._request("get")
        self.post = self._request("post")
        self.delete = self._request("delete")

        self._link_headers = None

    @staticmethod
    def _get_error_class(snake_code):
        module = import_module("fintoc.errors")
        pascal = snake_to_pascal(snake_code)

        # Hey, the following line of code may seem a bit puzzling, but...
        # it's not my fault that *just one* error code ends with "Error".
        # Anyway, we hope you never encounter that error.

        # Note to my future self: do yourself a favor and use Python 3.9!
        # >>> pascal.removesuffix("Error") + "Error"  (thank you, PEP616)
        class_ = pascal if pascal.endswith("Error") else pascal + "Error"
        return getattr(module, class_, "FintocError")

    def _request(self, method):
        def wrapper(resource, **kwargs):
            with self._client as client:
                response = client.request(method, resource, **kwargs)

            content = response.text and reduce(rename_keys, fieldsubs, response.json())
            if response.is_error:
                error = content.get("error")
                code = error.get("code")
                raise self._get_error_class(code)(error)

            self._link_headers = response.headers.get("link")
            return content

        return wrapper

    @property
    def link_headers(self):
        """
        Parse the link headers using some regex magic.
        """

        if self._link_headers is None:
            return None

        pattern = r'<(?P<url>.*)>;\s*rel="(?P<rel>.*)"'
        links = (link.strip() for link in self._link_headers.split(","))
        return dict(itemgetter("rel", "url")(re.match(pattern, link)) for link in links)

    def fetch_next(self):
        next_ = self.link_headers.get("next")  # I really miss you, walrus!
        while next_:
            yield self.get(next_)
            next_ = self.link_headers.get("next")

    def _get_link(self, link_token):
        return self.get(f"links/{link_token}")

    def _get_links(self):
        return self.get("links")

    def _post_link(self, credentials):
        return self.post("links", json=credentials, timeout=30)

    def _build_link(self, data):
        param = pick(data, "link_token")
        self._client.params.update(param)
        return Link(**data, _client=self)

    def get_link(self, link_token):
        data = {**self._get_link(link_token), "link_token": link_token}
        return self._build_link(data)

    def get_links(self):
        return map(self._build_link, self._get_links())

    def create_link(self, username, password, holder_type, institution_id):
        credentials = {
            "username": username,
            "password": password,
            "holder_type": holder_type,
            "institution_id": institution_id,
        }

        data = self._post_link(credentials)
        return self._build_link(data)

    def delete_link(self, link_id):
        self.delete(f"links/{link_id}")

    def get_account(self, *, link_token, account_id):
        return self.get_link(link_token).find(id_=account_id)

    def __str__(self):
        visible_chars = 4
        hidden_part = (len(self.api_key) - visible_chars) * "*"
        visible_key = self.api_key[-visible_chars:]
        return f"Client(🔑={hidden_part + visible_key})"
