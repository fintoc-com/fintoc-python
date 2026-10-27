---
name: add-api-resource
description: Add or update public v1/v2 API resources and actions in fintoc-python. Also use to assess whether new API fields require SDK changes.
---

# Add or update an API resource

## SDK model

Managers expose API operations and build request paths. Resources represent responses and provide instance behavior. The shared client handles HTTP, authentication, pagination, signing, and idempotency.

Reuse `ManagerMixin` and `ResourceMixin` for standard behavior. Extend them only where the API contract requires it, and expose only operations supported by that contract.

Use the relevant API contract from [main-api.json](https://github.com/fintoc-com/fintoc-docs/blob/main/reference/main-api.json) or [core-api.json](https://github.com/fintoc-com/fintoc-docs/blob/main/reference/core-api.json) in `fintoc-docs`.

## Choose the scope

| Change | Implementation |
| --- | --- |
| New resource | Add its manager and resource, export them (including the resource in `fintoc/resources/__init__.py`), and register the manager on the client for the appropriate API version. |
| New standard operation | Enable it on the existing manager when the shared implementation matches the contract. |
| New action | Implement `_<action>` and add the public name to `methods`. Use a trailing underscore for Python keywords. |
| Nested resource | Add the resource and manager, registering access on the parent manager. |
| New field | Usually no change: requests and responses accept fields dynamically. Use `ResourceMixin.mappings` when nested fields need a different resource class or list names do not singularize correctly. |

Resource classes are resolved only through `fintoc/resources/__init__.py`, not by API version or the versioned package exports. The PascalCase form of the manager's `resource` must match the exported name, including any alias; adding a v2 alias alone does not select it. Preserve v1 exports and verify the returned class, since missing exports silently produce a generic resource.

For custom action paths, reuse `_create(path_=...)` for POST, `_update(identifier, path_=...)` for PATCH, and `_upload` for multipart PUT when their response handling fits. Other request shapes need explicit handling through the shared client, preserving error translation and response conversion.

`_create(path_=...)` also assigns that path to the returned resource. If a new action returns a resource supporting instance updates or deletion, set its `_path` to the manager's resolved collection path before returning it, and test the subsequent operation. Keep this adjustment local to the new action; existing action bugs are separate work.

## Tests

Follow the existing pytest fixtures and conventions. Use integration tests to exercise the public client with mocked HTTP, checking request routing, parameter forwarding, and response conversion for the operations being added or changed. Assert the expected resource class with `isinstance`, including nested fields when relevant. Use dedicated response fixtures when the shared HTTP mock cannot represent the response shape.

Add focused manager or resource tests when introducing custom behavior. Cover relevant failure cases and subsequent instance operations when affected. Reuse shared transport coverage rather than duplicating authentication, signing, or idempotency tests for every resource.

Install dependencies with `poetry install`. Run the affected test files with `poetry run pytest tests/path_to_test.py`, optionally using `-k 'test_name'` to select tests. Then run the full suite and CI checks:

```sh
make tests
make black flake8 isort pylint
```

## Documentation and PR

Update the relevant README examples in English when public usage changes. Use `list`, not the deprecated `all`.

Follow the repository's PR template and record actual requirements or additional changes; use `None.` where there are none. Keep version bumps and releases separate from resource changes.
