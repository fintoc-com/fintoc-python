<h1 align="center">Fintoc meets Python 🐍</h1>

<p align="center">
    <em>
        You have just found the Python-flavored client of <a href="https://fintoc.com/" target="_blank">Fintoc</a>.
    </em>
</p>

<p align="center">
<a href="https://pypi.org/project/fintoc" target="_blank">
    <img src="https://img.shields.io/pypi/v/fintoc?label=version&logo=python&logoColor=%23fff&color=306998" alt="PyPI - Version">
</a>

<a href="https://github.com/fintoc-com/fintoc-python/actions?query=workflow%3Atests" target="_blank">
    <img src="https://img.shields.io/github/workflow/status/fintoc-com/fintoc-python/tests?label=tests&logo=python&logoColor=%23fff" alt="Tests">
</a>

<a href="https://codecov.io/gh/fintoc-com/fintoc-python" target="_blank">
    <img src="https://img.shields.io/codecov/c/gh/fintoc-com/fintoc-python?label=coverage&logo=codecov&logoColor=ffffff" alt="Coverage">
</a>

<a href="https://github.com/fintoc-com/fintoc-python/actions?query=workflow%3Alinters" target="_blank">
    <img src="https://img.shields.io/github/workflow/status/fintoc-com/fintoc-python/linters?label=linters&logo=github" alt="Linters">
</a>
</p>

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Quickstart](#quickstart)
  - [Calling endpoints](#calling-endpoints)
    - [list](#list)
    - [get](#get)
    - [create](#create)
    - [update](#update)
    - [delete](#delete)
    - [V2 Endpoints](#v2-endpoints)
    - [Nested actions or resources](#nested-actions-or-resources)
  - [Webhook Signature Validation](#webhook-signature-validation)
  - [Idempotency Keys](#idempotency-keys)
  - [Generate the JWS Signature](#gnerate-the-jws-signature)
  - [Serialization](#serialization)
- [Acknowledgements](#acknowledgements)

## Installation

Install using pip!

```sh
pip install fintoc
```

**Note:** This SDK requires [**Python 3.6+**](https://docs.python.org/3/whatsnew/3.6.html).

## Usage

The idea behind this SDK is to stick to the API design as much as possible, so that it feels ridiculously natural to use even while only reading the raw API documentation.

### Quickstart

To be able to use this SDK, you first need to get your secret API Key from the [Fintoc Dashboard](https://dashboard.fintoc.com/login). Once you have your API key, all you need to do is initialize a `Fintoc` object with it and you're ready to start enjoying Fintoc!

```python
from fintoc import Fintoc

client = Fintoc("your_api_key")

# list all succeeded payment intents since the beginning of 2025
payment_intents = client.payment_intents.list(since="2025-01-01", status="succeeded")
for pi in payment_intents:
    print(pi.created_at, pi.amount, pi.customer_email)

# Get a specific payment intent
payment_intent = client.payment_intents.get("pi_12345235412")
print(payment_intent.customer_email)
```

### Calling endpoints

The SDK provides direct access to Fintoc API resources following the API structure. Simply use the resource name and follow it by the appropriate action you want.

Notice that **not every resource has all of the methods**, as they correspond to the API capabilities.

#### `list`

You can use the `list` method to list all the instances of the resource:

```python
webhook_endpoints = client.webhook_endpoints.list()
```

The `list` method returns **a generator** with all the instances of the resource. This method can also receive the arguments that the API receives for that specific resource. For example, the `PaymentIntent` resource can be filtered using `since` and `until`, so if you wanted to get a range of `payment intents`, all you need to do is to pass the parameters to the method:

```python
payment_intents = client.payment_intents.list(since="2025-01-01", until="2025-02-01")
```

You can also pass the `lazy=False` parameter to the method to force the SDK to return a list of all the instances of the resource instead of the generator. **Beware**: this could take **very long**, depending on the amount of instances that exist of said resource:

```python
payment_intents = client.payment_intents.list(since="2025-01-01", until="2025-02-01", lazy=False)

isinstance(payment_intents, list)  # True
```

#### `get`

You can use the `get` method to get a specific instance of the resource:

```python
payment_intent = client.payment_intents.get("pi_8anqVLlBC8ROodem")
```

#### `create`

You can use the `create` method to create an instance of the resource:

```python
webhook_endpoint = client.webhook_endpoints.create(
    url="https://webhook.site/58gfb429-c33c-20c7-584b-d5ew3y3202a0",
    enabled_events=["link.credentials_changed"],
    description="Fantasting webhook endpoint",
)
```

The `create` method of the managers creates and returns a new instance of the resource. The attributes used for creating the object are passed as `kwargs`, and correspond to the parameters specified by the API documentation for the creation of said resource.

#### `update`

You can use the `update` method to update an instance of the resource:

```python
webhook_endpoint = client.webhook_endpoints.update(
    "we_8anqVLlBC8ROodem",
    enabled_events=["account.refresh_intent.succeeded"],
    disabled=True,
)
```

The `update` method updates and returns an existing instance of the resource using its identifier to find it. The first parameter of the method corresponds to the identifier being used to find the existing instance of the resource. The attributes to be modified are passed as `kwargs`, and correspond to the parameters specified by the API documentation for the update action of said resource.

#### `delete`

You can use the `delete` method to delete an instance of the resource:

```python
deleted_identifier = client.webhook_endpoints.delete("we_8anqVLlBC8ROodem")
```

The `delete` method deletes an existing instance of the resource using its identifier to find it and returns the identifier.

#### v2 Endpoints

To call v2 API endpoints, like the [Transfers API](https://docs.fintoc.com/reference/transfers), you need to prepend the resource name with the `v2` namespace, the same as the API does it:

```python
transfer = client.v2.transfers.create(
    amount=49523,
    currency="mxn",
    account_id="acc_123545",
    counterparty={"account_number": "014180655091438298"},
    metadata={"factura": "14814"},
)
```

#### Nested actions or resources

To call nested actions just call the method as it appears in the API. For example to [simulate receiving a transfer for the Transfers](https://docs.fintoc.com/reference/receive-an-inbound-transfer) product you can do:

```python
transfer = client.v2.simulate.receive_transfer(
    amount=9912400,
    currency="mxn",
    account_number_id="acno_2vF18OHZdXXxPJTLJ5qghpo1pdU",
)
```

### Webhook Signature Validation

To ensure the authenticity of incoming webhooks from Fintoc, you should always validate the signature. The SDK provides a `WebhookSignature` class to verify the `Fintoc-Signature` header

```python
WebhookSignature.verify_header(
    payload=request.get_data().decode('utf-8'),
    header=request.headers.get('Fintoc-Signature'),
    secret='your_webhook_secret'
)
```

The `verify_header` method takes the following parameters:
- `payload`: The raw request body as a string
- `header`: The Fintoc-Signature header value
- `secret`: Your webhook secret key (found in your Fintoc dashboard)
- `tolerance`: (Optional) Number of seconds to tolerate when checking timestamp (default: 300)

If the signature is invalid or the timestamp is outside the tolerance window, a `WebhookSignatureError` will be raised with a descriptive message.

For a complete example of handling webhooks, see [examples/webhook.py](examples/webhook.py).

### Idempotency Keys

You can provide an [Idempotency Key](https://docs.fintoc.com/reference/idempotent-requests) using the `idempotency_key` argument. For example:

```python
transfer = client.v2.transfers.create(
    idempotency_key="12345678910"
    amount=49523,
    currency="mxn",
    account_id="acc_123545",
    counterparty={"account_number": "014180655091438298"},
    metadata={"factura": "14814"},
)
```

### Generate the JWS Signature

Some endpoints need a [JWS Signature](https://docs.fintoc.com/docs/setting-up-jws-keys), in addition to your API Key, to verify the integrity and authenticity of API requests. To generate the signature, initialize the Fintoc client with the `jws_private_key` argument, and the SDK will handle the rest:

```python
import os

from fintoc import Fintoc

# Provide a path to your PEM file
client = Fintoc("your_api_key", jws_private_key="private_key.pem")

# Or pass the PEM key directly as a string
client = Fintoc("your_api_key", jws_private_key=os.environ.get('JWS_PRIVATE_KEY'))

# You can now create transfers securely
```


### Serialization

Any resource of the SDK can be serialized! To get the serialized resource, just call the `serialize` method!

```python
payment_intent = client.payment_intents.list(lazy=False)[0]

serialization = payment_intent.serialize()
```

The serialization corresponds to a dictionary with only simple types, that can be JSON-serialized.

## Acknowledgements

The first version of this SDK was originally designed and handcrafted by [**@nebil**](https://github.com/nebil),
[ad](https://en.wikipedia.org/wiki/Ad_honorem) [piscolem](https://en.wiktionary.org/wiki/piscola).
He built it with the help of Gianni Roberto's [Picchi 2](https://www.youtube.com/watch?v=WqjUlmkYr2g).
