"""Module for the methods that handle te resources."""

from fintoc.utils import objetize, objetize_generator


def resource_all(client, path, klass, handlers, methods, params):
    """Fetch all the instances of a resource."""
    lazy = params.pop("lazy", True)
    data = client.request(path, paginated=True, params=params)
    if lazy:
        return objetize_generator(
            data,
            klass,
            client,
            handlers=handlers,
            methods=methods,
            path=path,
        )
    return [
        objetize(
            klass,
            client,
            element,
            handlers=handlers,
            methods=methods,
            path=path,
        )
        for element in data
    ]


def resource_get(client, path, id_, klass, handlers, methods, params):
    """Fetch a specific instance of a resource."""
    data = client.request(f"{path}/{id_}", method="get", params=params)
    return objetize(
        klass,
        client,
        data,
        handlers=handlers,
        methods=methods,
        path=path,
    )


def resource_create(client, path, klass, handlers, methods, params):
    """Create a new instance of a resource."""
    data = client.request(path, method="post", json=params)
    return objetize(
        klass,
        client,
        data,
        handlers=handlers,
        methods=methods,
        path=path,
    )


def resource_update(client, path, id_, klass, handlers, methods, params):
    """Update a specific instance of a resource."""
    data = client.request(f"{path}/{id_}", method="patch", json=params)
    return objetize(
        klass,
        client,
        data,
        handlers,
        methods,
        path,
    )


def resource_delete(client, path, id_, params):
    """Delete an instance of a resource."""
    return client.request(f"{path}/{id_}", method="delete", params=params)
