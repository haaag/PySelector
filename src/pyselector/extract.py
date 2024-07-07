# extractor
from __future__ import annotations

import logging
from typing import Any
from typing import Callable
from typing import TypeVar

logger = logging.getLogger(__name__)

T = TypeVar('T')


def get_items_strings(
    items: list[Any],
    preprocessor: Callable[..., Any] | None = None,
) -> list[str]:
    if not items:
        return []
    preprocessor = preprocessor or str
    return list(filter(None, '\n'.join(map(preprocessor, items)).split('\n')))


def item(
    items: list[Any],
    selected: str,
    preprocessor: Callable[..., Any] | None = None,
) -> Any:
    """
    Parses selected items from a list based on a given string.

    Args:
        items (list[Any]): A list of items to search from.
        selected (str): A string containing selected items separated by newline characters.

    Returns:
        Any: Selected item
    """
    if not items and not selected:
        logger.debug('items and selected are empty')
        return None

    selected = selected.strip()

    try:
        items_str = get_items_strings(items, preprocessor)
        idx = items_str.index(selected)
        return items[idx]
    except ValueError as err:
        logger.debug(f'{err}. returning items={selected}')
    return None


def index(
    items: list[Any],
    selected: str,
    preprocessor: Callable[..., Any] | None = None,
) -> int:
    """
    Parses selected items from a list based on a given string.

    Args:
        items (list[Any]): A list of items to search from.
        selected (str): A string containing selected items separated by newline characters.

    Returns:
        int: Index of selected item, if not found returns -1
    """
    if not selected and not items:
        return -1

    selected = selected.strip()

    try:
        items = get_items_strings(items, preprocessor)
        return items.index(selected)
    except ValueError as err:
        logger.warning(f'{err}. Returning -1')
    return -1


def items(
    items: list[Any],
    selected: str,
    preprocessor: Callable[..., Any] | None = None,
) -> list[Any]:
    """
    Parses selected items from a list based on a given string.

    Args:
        items (list[Any]): A list of items to search from.
        selected (str): A string containing selected items separated by newline characters.

    Returns:
        list[Any]: A list containing selected items from the input list.
    """
    return parse_multiple_items(items, selected.strip(), preprocessor=preprocessor)


def indices(
    items: list[Any],
    selected: str,
    preprocessor: Callable[..., Any] | None = None,
) -> list[int]:
    """
    Parses selected items from a list based on a given string.

    Args:
        items (list[Any]): A list of items to search from.
        selected (str): A string containing selected items separated by newline characters.

    Returns:
        list[int]: A list containing their indices
    """
    return parse_multiple_items(items, selected.strip(), index=True, preprocessor=preprocessor)


def parse_multiple_items(
    items: list[Any],
    selected: str,
    index: bool = False,
    preprocessor: Callable[..., Any] | None = None,
):
    result: list[Any] = []
    if not items and not selected:
        logger.debug('items and selected are empty')
        return result

    try:
        items_str = get_items_strings(items, preprocessor)
        selected_clean = [item for item in selected.split('\n') if item]
        for selection in selected_clean:
            if selection not in items_str:
                continue
            idx = items_str.index(selection)
            if index:
                result.append(idx)
            else:
                result.append(items[idx])
    except ValueError as err:
        logger.warning(f'{err}. Returning items={selected}')
    return result
