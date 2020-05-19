"""
resources.py
============

All the resources offered by Fintoc.
"""

from functools import reduce
import json
from datetime import date, datetime
from dateutil.parser import isoparse
from tabulate import tabulate
from fintoc.utils import fieldsubs, flatten, pluralize, rename_keys


class ResourceMixin:
    """
    A mixin to share common perks between resource classes.
    """

    def __eq__(self, other):
        return self.id_ == other.id_

    def __hash__(self):
        return hash(self.id_)

    def __repr__(self):
        return f"<{self.__class__.__name__} @id={self.id_}>"

    @staticmethod
    def encoder(obj):
        if hasattr(obj, "serialize"):
            return obj.serialize()
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()

    def serialize(self):
        fields = vars(self).items()
        public = {attr: value for attr, value in fields if not attr.startswith("_")}
        output = json.dumps(public, default=self.encoder)
        inverted = (tuple(reversed(sub)) for sub in fieldsubs)
        return reduce(rename_keys, inverted, json.loads(output))


# The **kwargs enable a future-proof interface.
# pylint: disable=unused-argument

# There is a conflict between Pylint and Black.
# pylint: disable=bad-continuation


class Link(ResourceMixin):
    def __init__(
        self,
        id_,
        username,
        holder_type,
        institution,
        created_at,
        accounts=None,
        link_token=None,
        _client=None,
        **kwargs,
    ):
        self.id_ = id_
        self.username = username
        self.holder_type = holder_type
        self.institution = Institution(**institution)
        self.created_at = isoparse(created_at)
        self.accounts = [Account(**data, _client=_client) for data in accounts or []]
        self._token = link_token
        self._client = _client

    def find_all(self, **kwargs):
        if len(kwargs) != 1:
            raise ValueError("You must provide *exactly one* account field.")

        [(field, value)] = kwargs.items()
        return (account for account in self if getattr(account, field) == value)

    def find(self, **kwargs):
        return next(self.find_all(**kwargs), None)

    def show_accounts(self, rows=5):
        def get_row(index, account):
            return index, account.name, account.holder_name, account.currency

        print(f"This link has {pluralize(len(self), 'account')}.")

        if len(self) > 0:
            accounts = (get_row(*acc) for acc in enumerate(self.accounts[:rows]))
            headers = ("#", "Name", "Holder", "Currency")
            table = tabulate(accounts, headers=headers)
            print()
            print(table)

    def update_accounts(self):
        for account in self:
            account.update_balance()
            account.update_movements()

    def _delete(self):
        self._client.delete_link(self.id_)

    def __getitem__(self, index):
        return self.accounts[index]

    def __len__(self):
        return len(self.accounts)

    def __str__(self):
        return f"<{self.username}@{self.institution.name}> 🔗 <Fintoc>"


class Account(ResourceMixin):
    def __init__(
        self,
        id_,
        name,
        official_name,
        number,
        holder_id,
        holder_name,
        type_,
        currency,
        balance=None,
        movements=None,
        _client=None,
        **kwargs,
    ):
        self.id_ = id_
        self.name = name
        self.official_name = official_name
        self.number = number
        self.holder_id = holder_id
        self.holder_name = holder_name
        self.type_ = type_
        self.currency = currency
        self.balance = Balance(**balance)
        self.movements = movements or []
        self._client = _client

    def _get_account(self):
        return self._client.get(f"accounts/{self.id_}")

    def _get_movements(self, **params):
        first = self._client.get(f"accounts/{self.id_}/movements", params=params)
        return first + flatten(self._client.fetch_next()) if params else first

    def update_balance(self):
        data = self._get_account().get("balance")
        self.balance = Balance(**data)

    def get_movements(self, **params):
        return (Movement(**movement) for movement in self._get_movements(**params))

    def update_movements(self, **params):
        self.movements += list(self.get_movements(**params))
        # Remove some duplicates while preserving the order,
        # by using a CPython-powered, order-preserving dict.
        uniques = dict.fromkeys(self.movements)
        self.movements = sorted(uniques, key=lambda mov: mov.post_date, reverse=True)

    def show_movements(self, rows=5):
        def get_row(index, movement):
            return (
                index,
                f"{movement.amount:n}",
                movement.currency,
                movement.description,
                movement.locale_date,
            )

        print(f"This account has {pluralize(len(self), 'movement')}.")

        if len(self) > 0:
            movements = (get_row(*mov) for mov in enumerate(self.movements[:rows]))
            colalign = ("right", "right", "left", "left", "left")
            headers = ("#", "Amount", "Currency", "Description", "Date")
            table = tabulate(movements, headers=headers, colalign=colalign)
            print()
            print(table)

    def __getitem__(self, index):
        return self.movements[index]

    def __len__(self):
        return len(self.movements)

    def __str__(self):
        return f"💰 {self.holder_name}’s {self.name}"


class Movement(ResourceMixin):
    def __init__(
        self, id_, amount, currency, description, post_date, transaction_date, **kwargs
    ):
        self.id_ = id_
        self.amount = amount
        self.currency = currency
        self.description = description
        self.post_date = isoparse(post_date)
        self.transaction_date = isoparse(transaction_date)

    @property
    def locale_date(self):
        return self.post_date.strftime("%x")

    def __str__(self):
        return f"{self.amount:n} ({self.description} @ {self.locale_date})"


class Balance(ResourceMixin):
    def __init__(self, available, current, limit, **kwargs):
        self.available = available
        self.current = current
        self.limit = limit

    @property
    def id_(self):
        return id(self)

    def __str__(self):
        return f"{self.available:n} / {self.current:n}"


class Institution(ResourceMixin):
    def __init__(self, id_, name, country, **kwargs):
        self.id_ = id_
        self.name = name
        self.country = country

    def __str__(self):
        return f"🏦 {self.name}"
