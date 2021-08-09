import re
from functools import reduce

from fintoc.constants import LINK_HEADER_PATTERN


def paginate(client, path, params):
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
    response = client.get(path, params=params)
    response.raise_for_status()
    next_ = parse_link_headers(response.headers.get("link")).get("next")
    elements = response.json()
    return {
        "next": next_,
        "elements": elements,
    }


def parse_link_headers(link_header):
    if link_header is None:
        return None
    return reduce(parse_link, link_header.split(","), {})


def parse_link(dictionary, link):
    matches = re.match(LINK_HEADER_PATTERN, link.strip()).groupdict()
    dictionary[matches["rel"]] = matches["url"]
    return {**dictionary, matches["rel"]: matches["url"]}
