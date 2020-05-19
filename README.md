
# Fintoc meets :snake:

You have just found the [Python](https://www.python.org/)-flavored client of [Fintoc](https://fintoc.com/).

## Why?

You can think of [Fintoc API](https://fintoc.com/docs) as a piscola.
And the key ingredient to a properly made piscola are the ice cubes.  
Sure, you can still have a [piscola without ice cubes](https://curl.haxx.se/).
But hey… that’s not enjoyable -- why would you do that?  
Do yourself a favor: go grab some ice cubes by installing this refreshing library.

---

## Features

- Your bank account at your fingertips using idiomatic Python
- A minimalist user interface that feels like a [DSL](https://en.wikipedia.org/wiki/Domain-specific_language)
- Quite a few handpicked emoji

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
>>> account.update_movements()
>>> account.show_movements(10)
```

And that’s it!

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
