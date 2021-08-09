from fintoc.helpers import objetize, objetize_generator


def resource_all(client, path, klass, handlers, methods, params):
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
    return client.request(f"{path}/{id_}", method="delete", params=params)
