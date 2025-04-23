from types import GeneratorType

import httpx
import pytest

from fintoc.paginator import paginate, parse_link, parse_link_headers, request


class TestParseLink:
    def test_link_over_empty_dictionary(self):
        next_url = "https://api.fintoc.com/v1/links?page=2"
        dictionary = {}
        link = f'<{next_url}>; rel="next"'
        parsed = parse_link(dictionary, link)
        assert isinstance(parsed, dict)
        assert "next" in parsed
        assert len(parsed.keys()) == 1
        assert parsed["next"] == next_url

    def test_link_over_used_dictionary(self):
        next_url = "https://api.fintoc.com/v1/links?page=2"
        last_url = "https://api.fintoc.com/v1/links?page=13"
        dictionary = {"last": last_url}
        link = f'<{next_url}>; rel="next"'
        parsed = parse_link(dictionary, link)
        assert isinstance(parsed, dict)
        assert "last" in parsed
        assert "next" in parsed
        assert len(parsed.keys()) == 2
        assert parsed["last"] == last_url
        assert parsed["next"] == next_url

    def test_overwrite_dictionary(self):
        curr_url = "https://api.fintoc.com/v1/links?page=2"
        next_url = "https://api.fintoc.com/v1/links?page=4"
        last_url = "https://api.fintoc.com/v1/links?page=13"
        dictionary = {"next": curr_url, "last": last_url}
        link = f'<{next_url}>; rel="next"'
        parsed = parse_link(dictionary, link)
        assert isinstance(parsed, dict)
        assert "last" in parsed
        assert "next" in parsed
        assert len(parsed.keys()) == 2
        assert parsed["last"] == last_url
        assert parsed["next"] != curr_url
        assert parsed["next"] == next_url


class TestParseLinkHeaders:
    def test_empty_header(self):
        parsed = parse_link_headers(None)
        assert parsed is None

    def test_parse_header(self):
        next_url = "https://api.fintoc.com/v1/links?page=2"
        last_url = "https://api.fintoc.com/v1/links?page=13"
        link_header = f'<{next_url}>; rel="next", <{last_url}>; rel="last"'
        parsed = parse_link_headers(link_header)
        assert isinstance(parsed, dict)
        assert "next" in parsed
        assert "last" in parsed
        assert len(parsed.keys()) == 2
        assert parsed["next"] == next_url
        assert parsed["last"] == last_url


class TestRequest:
    @pytest.fixture(autouse=True)
    def patch_http_client(self, patch_http_client):
        pass

    def test_request_response(self):
        client = httpx.Client(base_url="https://test.com")
        data = request(client, "/movements")
        assert "next" in data
        assert "elements" in data
        assert isinstance(data["elements"], list)

    def test_request_params_get_passed_to_next_url(self):
        client = httpx.Client(base_url="https://test.com")
        data = request(client, "/movements", params={"link_token": "sample_link_token"})
        assert "next" in data
        assert "link_token=sample_link_token" in data["next"]


class TestPaginate:
    @pytest.fixture(autouse=True)
    def patch_http_client(self, patch_http_client):
        pass

    def test_pagination(self):
        client = httpx.Client(base_url="https://test.com")
        data = paginate(client, "/movements", {}, {})
        assert isinstance(data, GeneratorType)

        elements = list(data)
        assert len(elements) == 100

        for element in elements:
            assert isinstance(element, dict)
