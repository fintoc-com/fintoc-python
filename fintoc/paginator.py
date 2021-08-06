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


def objetize_generator(generator, client_data, klass):
    for element in generator:
        yield klass(client_data, **element)


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
    return reduce(lambda x, y: parse_link(x, y), link_header.split(","), {})


def parse_link(dictionary, link):
    matches = re.match(LINK_HEADER_PATTERN, link.strip()).groupdict()
    dictionary[matches["rel"]] = matches["url"]
    return {**dictionary, matches["rel"]: matches["url"]}
