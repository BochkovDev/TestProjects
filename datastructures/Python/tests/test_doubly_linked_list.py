import pytest
from doubly_linked_list import DoublyLinkedList


@pytest.fixture
def empty_list():
    return DoublyLinkedList()


@pytest.fixture
def filled_list():
    lst = DoublyLinkedList()
    lst.extend([1, 2, 3])
    return lst


@pytest.mark.parametrize("values,expected", [
    ([1], [1]),
    ([1, 2, 3], [1, 2, 3]),
    ([], []),
])
def test_append(empty_list, values, expected):
    for value in values:
        empty_list.append(value)
    assert list(empty_list) == expected


@pytest.mark.parametrize("values,expected", [
    ([1], [1]),
    ([1, 2, 3], [3, 2, 1]),
    ([], []),
])
def test_prepend(empty_list, values, expected):
    for value in values:
        empty_list.prepend(value)
    assert list(empty_list) == expected


@pytest.mark.parametrize("index, value, expected", [
    (0, 1, [1, 1, 2, 3]),
    (1, 4, [1, 4, 2, 3]),
    (2, 5, [1, 2, 5, 3]),
])
def test_insert(filled_list, index, value, expected):
    filled_list.insert(index, value)
    assert list(filled_list) == expected


@pytest.mark.parametrize("values,expected", [
    ([4, 5], [1, 2, 3, 4, 5]),
    ([6], [1, 2, 3, 6]),
    ([], [1, 2, 3]),
])
def test_extend(filled_list, values, expected):
    filled_list.extend(values)
    assert list(filled_list) == expected


@pytest.mark.parametrize("value, expected", [
    (1, [2, 3]),
    (2, [1, 3]),
    (3, [1, 2]),
    (4, [1, 2, 3]),
])
def test_delete(filled_list, value, expected):
    filled_list.delete(value)
    assert list(filled_list) == expected


@pytest.mark.parametrize("index, expected", [
    (0, [2, 3]),
    (1, [1, 3]),
    (2, [1, 2]),
    (3, [1, 2, 3]),  
])
def test_delete_at(filled_list, index, expected):
    try:
        filled_list.delete_at(index)
    except IndexError:
        assert list(filled_list) == expected
    else:
        assert list(filled_list) == expected


@pytest.mark.parametrize("initial_values,expected", [
    ([1, 1, 2, 2, 3, 3], [1, 2, 3]),
    ([1, 2, 3], [1, 2, 3]),
    ([1, 1, 1], [1]),
])
def test_remove_duplicates(initial_values, expected):
    lst = DoublyLinkedList()
    lst.extend(initial_values)
    lst.remove_duplicates()
    assert list(lst) == expected


def test_clear(filled_list):
    filled_list.clear()
    assert filled_list.head == None
    assert filled_list.tail == None


@pytest.mark.parametrize("value, expected", [
    (1, 0),
    (2, 1),
    (3, 2),
    (4, None),
])
def test_find(filled_list, value, expected):
    assert filled_list.find(value) == expected


@pytest.mark.parametrize("initial_values,expected", [
    ([1, 2, 3], [3, 2, 1]),
    ([1], [1]),
    ([], []),
])
def test_reverse(initial_values, expected):
    lst = DoublyLinkedList()
    lst.extend(initial_values)
    lst.reverse()
    assert list(lst) == expected


def test_get_set_item(filled_list):
    assert filled_list[1] == 2
    filled_list[1] = 4
    assert filled_list[1] == 4


def test_del_item(filled_list):
    del filled_list[1]
    assert list(filled_list) == [1, 3]


def test_add(filled_list):
    list1 = DoublyLinkedList()
    list1.extend([4, 5])
    new_list = filled_list + list1
    assert list(new_list) == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("value, expected", [
    (2, True),
    (4, False),
])
def test_contains(filled_list, value, expected):
    assert (value in filled_list) == expected


def test_len(filled_list):
    assert len(filled_list) == 3


def test_eq():
    list1 = DoublyLinkedList()
    list2 = DoublyLinkedList()
    list1.extend([1, 2, 3])
    list2.extend([1, 2, 3])
    assert list1 == list2

    list2.append(4)
    assert list1 != list2


def test_iter_reversed(filled_list):
    assert list(iter(filled_list)) == [1, 2, 3]
    assert list(reversed(filled_list)) == [3, 2, 1]