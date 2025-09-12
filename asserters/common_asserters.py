from typing import TypeVar

T = TypeVar("T")

def assert_list_contains_all(container: list[T], sublist: list[T]):
    missing = [item for item in sublist if item not in container]
    assert not missing, f"Список {container} не содержит элементы {missing}"