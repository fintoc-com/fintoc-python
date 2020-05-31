
# Fintoc meets :snake:
![PyPI - Version](https://img.shields.io/pypi/v/fintoc)
![PyPI - Downloads](https://img.shields.io/pypi/dm/fintoc)

You have just found the [Python](https://www.python.org/)-flavored client of [Fintoc](https://fintoc.com/).

## Why?

You can think of [Fintoc API](https://fintoc.com/docs) as a piscola.
And the key ingredient to a properly made piscola are the ice cubes.  
Sure, you can still have a [piscola without ice cubes](https://curl.haxx.se/).
But hey… that’s not enjoyable -- why would you do that?  
Do yourself a favor: go grab some ice cubes by installing this refreshing library.

---

## Table of contents

* [How to install](#how-to-install)
* [Quickstart](#quickstart)
* [Documentation](#documentation)
* [Examples](#examples)
  + [Get accounts](#get-accounts)
  + [Get movements](#get-movements)
* [Dependencies](#dependencies)
* [How to test...](#how-to-test)
* [Roadmap](#roadmap)
* [Acknowledgements](#acknowledgements)

## How to install

Install it with [Poetry](https://python-poetry.org/), the modern package manager.

```sh
$ poetry add fintoc
```

Don’t worry: if poetry is not your thing, you can also use [pip](https://pip.pypa.io/en/stable/).

```sh
$ pip install fintoc
```

**Note:** This client requires [**Python 3.6+**](https://docs.python.org/3/whatsnew/3.6.html).

## Quickstart

1. Get your API key and link your bank account using the [Fintoc dashboard](https://app.fintoc.com/login).
2. Open your command-line interface.
3. Write a few lines of Python to see your bank movements.

```python
>>> from fintoc import Client
>>> client = Client("your_api_key")
>>> link = client.get_link("your_link_token")
>>> account = link.find(type_="checking_account")
>>> account.get_movements(since='2020-01-01')
```

And that’s it!

## Documentation

This client supports all Fintoc API endpoints. For complete information about the API, head to the [docs](https://fintoc.com/docs).

## Examples

### Get accounts

```python
from fintoc import Client

client = Client("your_api_key")
link = client.get_link("your_link_token")

for account in link:
    print(account.name)

# Or... you can pretty print all the accounts in a Link
link.show_accounts()
```

If you want to find a specific account in a link, you can use **find**. You can search by any account field:

```python
account = link.find(type_="checking_account")
account = link.find(number="1111111")
account = link.find(id_="sdfsdf234")
```

You can also search for multiple accounts matching a specific criteria with **find_all**:

```python
clp_accounts = link.find_all(currency="CLP")
```

To update the account balance you can use **update_balance**:

```python
account.update_balance()
print(account.balance.available)
```

### Get movements

```python
from datetime import date, timedelta
from fintoc import Client

client = Client("your_api_key")
link = client.get_link("your_link_token")
account = link.find(type_="checking_account")

# You can get the account movements since a specific datetime
yesterday = date.today() - timedelta(days=1)
movements = account.get_movements(since=yesterday)

# Or... you can use an ISO 8601 formatted string representation of the datetime
movements = account.get_movements(since='2020-01-01')
```

Calling **get_movements** without arguments gets the last 30 movements of the account.

## Dependencies

This project relies on these useful libraries.

- [**httpx**](https://github.com/encode/httpx) -- a next-generation HTTP client
- [**tabulate**](https://github.com/astanin/python-tabulate) -- pretty-print tabular data
- [**python-dateutil**](https://github.com/dateutil/dateutil) -- useful extensions to the standard Python datetime features

## How to test…

### The web API

That’s a [🍰](https://en.wiktionary.org/wiki/piece_of_cake).

1. Log in into your bank account and send me some money.
2. Use this library to check if the movement is correct.
3. You’re welcome.

### The library

You can run all the [discoverable tests](https://docs.python.org/3/library/unittest.html#test-discovery).

`$ python -m unittest`

## Roadmap

- Add more docstrings
- Add more unit tests
- Add more type hints

## Acknowledgements

This library was initially designed and handcrafted by [**@nebil**](https://github.com/nebil),
[ad](https://en.wikipedia.org/wiki/Ad_honorem) [piscolem](https://en.wiktionary.org/wiki/piscola).  
He built it with the help of Gianni Roberto’s [Picchi 2](https://www.youtube.com/watch?v=WqjUlmkYr2g).
