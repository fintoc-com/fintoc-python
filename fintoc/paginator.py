"""Module to hold every utility used for pagination purposes."""

import re
from functools import reduce

from fintoc.constants import LINK_HEADER_PATTERN


def paginate(client, path, params):
    """
    Fetch a paginated resource and return a generator with all of
    its instances.
    """
    response = request(client, path, params=params)
    elements = response["elements"]
    for element in elements:
        yield element
    while response.get("next"):
        response = request(client, response.get("next"))
        elements = response["elements"]
        for element in elements:
            yield element


def request(client, path, params={}):
    """
    Fetch a page of a resource and return its elements and the next
    page of the resource.
    """
    response = client.request("get", path, params=params)
    response.raise_for_status()
    headers = parse_link_headers(response.headers.get("link"))
    next_ = headers and headers.get("next")
    elements = response.json()
    return {
        "next": next_,
        "elements": elements,
    }


def parse_link_headers(link_header):
    """
    Receive the 'link' header and return a dictionary with
    every key: value instance present on the header.
    """
    if link_header is None:
        return None
    return reduce(parse_link, link_header.split(","), {})


def parse_link(dictionary, link):
    """
    Receive a dictionary with already parsed key: values from the
    'link' header along with another link and return the original
    dictionary with a new entry corresponding to the link received.
    """
    matches = re.match(LINK_HEADER_PATTERN, link.strip()).groupdict()
    dictionary[matches["rel"]] = matches["url"]
    return {**dictionary, matches["rel"]: matches["url"]}
