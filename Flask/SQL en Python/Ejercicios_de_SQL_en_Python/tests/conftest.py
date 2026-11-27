LAYER_ORDER = ("_repository", "_service", "_rules", "_routes")


def _sort_key(item):
    path = item.path
    if "integration" in path.parts:
        return (len(LAYER_ORDER) + 1, 0)
    for index, suffix in enumerate(LAYER_ORDER):
        if path.stem.endswith(suffix):
            return (index, 0)
    return (len(LAYER_ORDER), 0)


def pytest_collection_modifyitems(items):
    """Unitarias primero (repositories, services, rules, routes) y al final las de integración."""
    items.sort(key=_sort_key)
