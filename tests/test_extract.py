# test_extract.py

from typing import Any
from typing import NamedTuple
from typing import Union

import pytest
from pyselector import extract

ITEMS = ['apple', 'banana', 'cherry', 'orange', 'grape', 'kiwi']


class Case(NamedTuple):
    name: str
    input: list[Any]
    selected: str
    expected: Union[Any, int, list[Any], list[int]]


@pytest.mark.parametrize(
    '_, input, selected, expected',
    [
        Case(
            name='single item',
            input=ITEMS,
            selected='kiwi',
            expected='kiwi',
        ),
        Case(
            name='single item not in items',
            input=ITEMS,
            selected='strawberry',
            expected=None,
        ),
        Case(
            name='no selected',
            input=ITEMS,
            selected='',
            expected=None,
        ),
        Case(
            name='no input',
            input=[],
            selected='kiwi',
            expected=None,
        ),
        Case(
            name='no input no selected',
            input=[],
            selected='',
            expected=None,
        ),
    ],
)
def test_extract_item(_, input, selected, expected):
    assert extract.item(input, selected) == expected


@pytest.mark.parametrize(
    '_, input, selected, expected',
    [
        Case(
            name='single item',
            input=ITEMS,
            selected='kiwi',
            expected=5,
        ),
        Case(
            name='single item',
            input=ITEMS,
            selected='apple',
            expected=0,
        ),
        Case(
            name='single item',
            input=ITEMS,
            selected='cherry',
            expected=2,
        ),
        Case(
            name='not found item',
            input=ITEMS,
            selected='strawberry',
            expected=-1,
        ),
        Case(
            name='not found item',
            input=ITEMS,
            selected='carrot',
            expected=-1,
        ),
        Case(
            name='empty input',
            input=ITEMS,
            selected='',
            expected=-1,
        ),
    ],
)

def test_extract_index(_, input, selected, expected):
    assert extract.index(input, selected) == expected


@pytest.mark.parametrize(
    '_, input, selected, expected',
    [
        Case(
            name='multiple items',
            input=ITEMS,
            selected='apple\nkiwi',
            expected=['apple', 'kiwi'],
        ),
        Case(
            name='multiple items found and one not found item',
            input=ITEMS,
            selected='banana\nstrawberry\ncherry\napple',
            expected=['banana', 'cherry', 'apple'],
        ),
        Case(
            name='multiple items not found',
            input=ITEMS,
            selected='strawberry\nmango\npineapple',
            expected=[],
        ),
        Case(
            name='empty items',
            input=[],
            selected='banana\ncherry',
            expected=[],
        ),
        Case(
            name='empty input',
            input=ITEMS,
            selected='',
            expected=[],
        ),
    ],
)
def test_extract_items(_, input, selected, expected):
    assert extract.items(input, selected) == expected


@pytest.mark.parametrize(
    '_, input, selected, expected',
    [
        Case(
            name='multiple indexes',
            input=ITEMS,
            selected='apple\nkiwi',
            expected=[0, 5],
        ),
        Case(
            name='multiple indexes found and one not found item',
            input=ITEMS,
            selected='banana\nstrawberry\ncherry\napple',
            expected=[1, 2, 0],
        ),
        Case(
            name='multiple indexes not found',
            input=ITEMS,
            selected='strawberry\nmango\npineapple',
            expected=[],
        ),
        Case(
            name='empty items',
            input=[],
            selected='banana\ncherry',
            expected=[],
        ),
        Case(
            name='empty input',
            input=ITEMS,
            selected='',
            expected=[],
        ),
    ],
)
def test_extract_indices(_, input, selected, expected):
    assert extract.indices(input, selected) == expected
