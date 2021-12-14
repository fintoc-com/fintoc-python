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

## Why?

You can think of [Fintoc API](https://fintoc.com/docs) as a piscola.
And the key ingredient to a properly made piscola are the ice cubes.
Sure, you can still have a [piscola without ice cubes](https://curl.haxx.se/).
But hey… that’s not enjoyable -- why would you do that?
Do yourself a favor: go grab some ice cubes by installing this refreshing library.

## Installation

Install using pip!

```sh
pip install fintoc
```

**Note:** This SDK requires [**Python 3.6+**](https://docs.python.org/3/whatsnew/3.6.html).

## Usage

The idea behind this SDK is to stick to the API design as much as possible, so that it feels ridiculously natural to use even while only reading the raw API documentation.

### Quickstart

To be able to use this SDK, you first need to have a [Fintoc](https://app.fintoc.com/login) account. You will need to get your secret API key from the dashboard to be able to use the SDK. Once you have your API key, all you need to do is initialize a `Fintoc` object with it and you're ready to start enjoying Fintoc!

```python
from fintoc import Fintoc

fintoc_client = Fintoc("your_api_key")
```

Now you can start using the SDK!

### Managers

To make the usage of the SDK feel natural, resources are managed by **managers** (_wow_). These **managers** correspond to objects with some methods that allow you to get the resources that you want. Each manager is _attached_ to another resource, following the API structure. For example, the `Fintoc` object has `links` and `webhook_endpoints` managers, while `Link` objects have an `accounts` manager (we will see more examples soon). Notice that **not every manager has all of the methods**, as they correspond to the API capabilities. The methods of the managers are the following (we will use the `webhook_endpoints` manager as an example):

#### `all`

You can use the `all` method of the managers as follows:

```python
webhook_endpoints = fintoc_client.webhook_endpoints.all()
```

The `all` method of the managers returns **a generator** with all the instances of the resource. This method can also receive `kwargs`! The arguments that can be passed are the arguments that the API receives for that specific resource! For example, the `Movement` resource can be filtered using `since` and `until`, so if you wanted to get a range of `movements` from an `account`, all you need to do is to pass the parameters to the method!

```python
movements = account.movements.all(since="2019-07-24", until="2021-05-12")
```

You can also pass the `lazy=False` parameter to the method to force the SDK to return a list of all the instances of the resource instead of the generator. **Beware**: this could take **very long**, depending on the amount of instances that exist of said resource:

```python
webhook_endpoints = fintoc_client.webhook_endpoints.all(lazy=False)

isinstance(webhook_endpoints, list)  # True
```

#### `get`

You can use the `get` method of the managers as follows:

```python
webhook_endpoint = fintoc_client.webhook_endpoints.get("we_8anqVLlBC8ROodem")
```

The `get` method of the managers returns an existing instance of the resource using its identifier to find it.

#### `create`

You can use the `create` method of the managers as follows:

```python
webhook_endpoint = fintoc_client.webhook_endpoints.create(
    url="https://webhook.site/58gfb429-c33c-20c7-584b-d5ew3y3202a0",
    enabled_events=["link.credentials_changed"],
    description="Fantasting webhook endpoint",
)
```

The `create` method of the managers creates and returns a new instance of the resource. The attributes of the created object are passed as `kwargs`, and correspond to the parameters specified by the API documentation for the creation of said resource.

#### `update`

You can use the `update` method of the managers as follows:

```python
webhook_endpoint = fintoc_client.webhook_endpoints.update(
    "we_8anqVLlBC8ROodem",
    enabled_events=["account.refresh_intent.succeeded"],
    disabled=True,
)
```

The `update` method of the managers updates and returns an existing instance of the resource using its identifier to find it. The first parameter of the method corresponds to the identifier being used to find the existing instance of the resource. The attributes to be modified are passed as `kwargs`, and correspond to the parameters specified by the API documentation for the update action of said resource.

Notice that using the manager to update an instance of a resource is equivalent (in terms of outcome) to calling the `update` directly on the object itself:


```python
# Using the manager
webhook_endpoint = fintoc_client.webhook_endpoints.update(
    "we_8anqVLlBC8ROodem",
    enabled_events=["account.refresh_intent.succeeded"],
    disabled=True,
)

# Using the object
webhook_endpoint = fintoc_client.webhook_endpoints.get("we_8anqVLlBC8ROodem")
webhook_endpoint.update(
    enabled_events=["account.refresh_intent.succeeded"],
    disabled=True,
)
```

When using the SDK, you will probably almost always want to use the object directly to update, just because it is way less verbose if you already have the object itself. Also, using the `update` method from the manager first needs to `get` the resource and then updates it, so it translates to 2 API calls. If you already have the object to update, using the `update` method directly from the object just updates it, so it translates to just 1 API call.

#### `delete`

You can use the `delete` method of the managers as follows:

```python
deleted_identifier = fintoc_client.webhook_endpoints.delete("we_8anqVLlBC8ROodem")
```

The `delete` method of the managers deletes an existing instance of the resource using its identifier to find it and returns the identifier.

Notice that using the manager to delete an instance of a resource is equivalent (in terms of outcome) to calling the `delete` directly on the object itself:


```python
# Using the manager
deleted_identifier = fintoc_client.webhook_endpoints.delete("we_8anqVLlBC8ROodem")

# Using the object
webhook_endpoint = fintoc_client.webhook_endpoints.get("we_8anqVLlBC8ROodem")
deleted_identifier = webhook_endpoint.delete()
```

When using the SDK, you will probably almost always want to use the object directly to delete, just because it is way less verbose if you already have the object itself. Also, using the `delete` method from the manager first needs to `get` the resource and then deletes it, so it translates to 2 API calls. If you already have the object to delete, using the `delete` method directly from the object just deletes it, so it translates to just 1 API call.

### The shape of the SDK

For complete information about the API, head to [the docs](https://fintoc.com/docs). You will notice that the shape of the SDK is very similar to the shape of the API. Let's start with the `Fintoc` object.

#### The `Fintoc` object

To create a `Fintoc` object, instantiate it using your secret API key:

```python
from fintoc import Fintoc

fintoc_client = Fintoc("your_api_key")
```

This gives us access to a bunch of operations already. The object created using this _snippet_ contains three [managers](#managers): `links`, `payment_intents` and `webhook_endpoints`.

#### The `webhook_endpoints` manager

Available methods: `all`, `get`, `create`, `update`, `delete`.

From the Fintoc client, you can manage your webhook endpoints swiftly! Start by creating a new Webhook Endpoint!

```python
webhook_endpoint = fintoc_client.webhook_endpoints.create(
    url="https://webhook.site/58gfb429-c33c-20c7-584b-d5ew3y3202a0",
    enabled_events=["account.refresh_intent.succeeded"],
    disabled=True,
)

print(webhook_endpoint.id)  # we_8anqVLlBC8ROodem
```

You can update this webhook endpoint any time you want! Just run the following command:

```python
webhook_endpoint = fintoc_client.webhook_endpoints.update(
    "we_8anqVLlBC8ROodem",
    enabled_events=["link.credentials_changed"],
    description="Fantasting webhook endpoint",
)

print(webhook_endpoint.status)  # disabled
```

Maybe you no longer want this webhook endpoint. Let's delete it!

```python
fintoc_client.webhook_endpoints.delete("we_8anqVLlBC8ROodem")
```

Now, let's list every webhook endpoint we have:

```python
for webhook_endpoint in fintoc_client.webhook_endpoints.all():
    print(webhook_endpoint.id)
```

If you see a webhook endpoint you want to use, just use the `get` method!

```python
webhook_endpoint = fintoc_client.webhook_endpoints.get("we_8anqVLlBC8ROodem")

print(webhook_endpoint.id)  # we_8anqVLlBC8ROodem
```

#### The `payment_intents` manager

Available methods: `all`, `get`, `create`.

Payment intents allow you to start a payment using Fintoc! Start by creating a new payment intent:

```python
payment_intent = fintoc_client.payment_intents.create(
    currency="CLP",
    amount=5990,
    recipient_account={
        "holder_id": "111111111",
        "number": "123123123",
        "type": "checking_account",
        "institution_id": "cl_banco_de_chile",
    }
)

print(payment_intent.id)            # pi_BO381oEATXonG6bj
print(payment_intent.widget_token)  # pi_BO381oEATXonG6bj_sec_a4xK32BanKWYn
```

Notice that the success of this payment intent will be notified through a Webhook. Now, let's list every payment intent we have:

```python
for payment_intent in fintoc_client.payment_intents.all():
    print(payment_intent.id)
```

If you see a payment intent you want to use, just use the `get` method!

```python
payment_intent = fintoc_client.payment_intents.get("pi_BO381oEATXonG6bj")

print(payment_intent.id)      # pi_BO381oEATXonG6bj
print(payment_intent.status)  # succeeded
```

#### The `links` manager

Available methods: `all`, `get`, `update`, `delete`.

Links are probably the most importat resource. Let's list them!

```python
print(len(fintoc_client.links.all(lazy=False)))  # 3

for link in fintoc_client.links.all():
    print(link.id)
```

Links are a bit different than the rest of the resources, because their identifier is not really their `id`, but their `link_token`. This means that, in order to `get`, `update` or `delete` a link, you need to pass the `link_token`!

```python
link = fintoc_client.links.get("link_Y75EXAKiIVj7w489_token_NCqjwRVoTX3cmnx8pnbpqd11")
```

Notice that the Link objects generated from the `all` method will won't be able to execute `update` or `delete` operations, while any Link object generated from `get` or `update` will have permission to `update` or `delete` (given that the link token is necessary to `get` or `update` in the first place).

The Link resource has a lot of **managers**!

```python
invoices = link.invoices.all()  # Invoices
tax_returns = link.tax_returns.all()  # Tax Returns
subscriptions = link.subscriptions.all()  # Subscriptions
refresh_intents = link.refresh_intents.all()  # Refresh Intents
accounts = link.accounts.all()  # Accounts
```

#### The `invoices` manager

Available methods: `all`.

Once you have a Link, you can use the `invoices` manager to get all the invoices associated to a link!

```python
for invoice in link.invoices.all():
    print(invoice.id)
```

#### The `tax_returns` manager

Available methods: `all`, `get`.

Once you have a Link, you can use the `tax_returns` manager to get all the tax returns associated to a link!

```python
for tax_return in link.tax_returns.all():
    print(tax_return.id)
```

#### The `subscriptions` manager

Available methods: `all`, `get`.

Once you have a Link, you can use the `subscriptions` manager to get all the subscriptions associated to a link!

```python
for subscription in link.subscriptions.all():
    print(subscription.id)
```

#### The `refresh_intents` manager

Available methods: `all`, `get`, `create`.

Refresh intents allow you to control how an account gets refreshed on Fintoc! Once you have a Link, you can use the `refresh_intents` manager to create a new refresh intent:

```python
refresh_intent = link.refresh_intents.create()

print(refresh_intent.id)  # ri_5A94DVCJ7xNM3MEo
```

Notice that the success of this refresh intent will be notified through a Webhook. Now, let's list every refresh intent we have:

```python
for refresh_intent in link.refresh_intents.all():
    print(refresh_intent.id)
```

If you see a refresh intent you want to use, just use the `get` method!

```python
refresh_intent = link.refresh_intents.get("ri_5A94DVCJ7xNM3MEo")

print(refresh_intent.id)      # ri_5A94DVCJ7xNM3MEo
print(refresh_intent.status)  # succeeded
```

#### The `accounts` manager

Available methods: `all`, `get`.

Once you have a Link, you can use the `accounts` manager to get all the accounts associated to a link!

```python
for account in link.accounts.all():
    print(account.id)
```

Notice that accounts also have a `movements` manager, to get all of the movements of an account:

```python
account = link.accounts.all(lazy=False)[0]

movements = account.movements.all(lazy=False)
```

#### The `movements` manager

Available methods: `all`, `get`.

Once you have an Account, you can use the `movements` manager to get all the movements associated to that account!

```python
for movement in account.movements.all():
    print(movement.id)
```

### Serialization

Any resource of the SDK can be serialized! To get the serialized resource, just call the `serialize` method!

```python
account = link.accounts.all(lazy=False)[0]

serialization = account.serialize()
```

The serialization corresponds to a dictionary with only simple types, that can be JSON-serialized.

## Acknowledgements

The first version of this SDK was originally designed and handcrafted by [**@nebil**](https://github.com/nebil),
[ad](https://en.wikipedia.org/wiki/Ad_honorem) [piscolem](https://en.wiktionary.org/wiki/piscola).
He built it with the help of Gianni Roberto’s [Picchi 2](https://www.youtube.com/watch?v=WqjUlmkYr2g).
