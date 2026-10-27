"""Recipients requests through the public v2 client."""

import json
from pathlib import Path

import httpx
import pytest

from fintoc.client import Client
from fintoc.core import Fintoc
from fintoc.resources.v2 import Recipient


@pytest.fixture(params=["mx", "cl"])
def payload(request):
    path = Path(__file__).parent / "fixtures" / f"recipient_{request.param}.json"
    return json.loads(path.read_text())


@pytest.fixture
def api(monkeypatch, payload):
    requests = []

    def respond(request):
        requests.append(request)
        if request.method == "DELETE":
            return httpx.Response(204)
        if request.method == "GET" and request.url.path == "/v2/recipients":
            headers = {}
            if "starting_after" not in request.url.params:
                headers["link"] = (
                    "<https://api.fintoc.com/v2/recipients?starting_after="
                    + payload["id"]
                    + '>; rel="next"'
                )
            return httpx.Response(200, json=[payload], headers=headers)
        updates = json.loads(request.content) if request.method == "PATCH" else {}
        return httpx.Response(200, json={**payload, **updates})

    with httpx.Client(transport=httpx.MockTransport(respond)) as transport:
        monkeypatch.setattr(Client, "_client", transport)
        yield Fintoc("sk_test_recipients").v2.recipients, requests


def test_create(api, payload):
    recipients, requests = api
    params = {
        key: payload[key]
        for key in ("account_number", "holder_name", "holder_type", "holder_id")
    }
    params["entity_id"] = "ent_test"
    if payload["institution"]["country"] == "cl":
        params.update(
            institution_id=payload["institution"]["id"],
            account_type=payload["account_type"],
        )
    recipient = recipients.create(idempotency_key="recipient-create", **params)

    assert isinstance(recipient, Recipient)
    assert recipient.serialize() == payload
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/v2/recipients"
    assert requests[0].headers["Idempotency-Key"] == "recipient-create"
    assert json.loads(requests[0].content) == params


def test_get(api, payload):
    recipients, requests = api
    recipient = recipients.get(payload["id"])

    assert isinstance(recipient, Recipient)
    assert recipient.serialize() == payload
    assert requests[0].url.path == f'/v2/recipients/{payload["id"]}'


@pytest.mark.parametrize("lazy", [True, False])
def test_list_filters_and_pagination(api, payload, lazy):
    recipients, requests = api
    filters = {
        "entity_id": "ent_test",
        "holder_type": "person",
        "institution_id": payload["institution"]["id"],
        "holder_id": payload["holder_id"],
        "account_number": payload["account_number"],
        "ending_before": "rcp_previous",
        "limit": 1,
    }
    result = list(recipients.list(lazy=lazy, **filters))

    assert len(result) == 2
    assert all(isinstance(recipient, Recipient) for recipient in result)
    assert dict(requests[0].url.params) == {k: str(v) for k, v in filters.items()}
    assert requests[1].url.params["starting_after"] == payload["id"]


@pytest.mark.parametrize(
    "updates",
    [
        {"alias": None, "email": None},
        {"alias": "", "email": ""},
        {"holder_name": "New name"},
    ],
)
@pytest.mark.parametrize("on_resource", [False, True])
def test_update(api, payload, updates, on_resource):
    recipients, requests = api
    if on_resource:
        recipient = recipients.get(payload["id"])
        result = recipient.update(**updates)
        assert result is recipient
    else:
        result = recipients.update(payload["id"], **updates)

    assert isinstance(result, Recipient)
    assert result.serialize() == {**payload, **updates}
    assert requests[-1].method == "PATCH"
    assert requests[-1].url.path == f'/v2/recipients/{payload["id"]}'
    assert json.loads(requests[-1].content) == updates


@pytest.mark.parametrize("on_resource", [False, True])
def test_delete_empty_response(api, payload, on_resource):
    recipients, requests = api
    result = (
        recipients.get(payload["id"]).delete()
        if on_resource
        else recipients.delete(payload["id"])
    )

    assert result == payload["id"]
    assert requests[-1].method == "DELETE"
    assert requests[-1].url.path == f'/v2/recipients/{payload["id"]}'
