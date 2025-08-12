"""
To create an iterator in Python, there are two abstract classes from the built-in
'collections' module - Iterable, Iterator. We need to implement the
`__iter__()` method in the iterated object (collection), and the `__next__()`
method in the iterator.
"""
from collections.abc import Iterator, Iterable
from typing import Any


class AlphabeticalOrderIterator(Iterator):
    """
    Concrete Iterators implement various traversal algorithms.
    These classes store the current traversal position at all times.
    """

    """
    `_position` attribute stores the current traversal position. An iterator may
    have a lot of other fields for storing iteration state, especially when it 
    is supposed to work with a particular kind of collection.
    """
    _position: int = None

    """
    This attribute indicates the traversal direction.
    """
    _reverse: bool = False

    def __init__(self, collection: 'WordCollection', reverse: bool = False) -> None:
        self._collection = collection
        self._reverse = reverse
        self._sorted_items = None  # Will be set on first __next__ call
        self._position = 0

    def __next__(self) -> Any:
        """
        Optimization: sorting happens only when the first items is actually requested.
        """
        if self._sorted_items is None:
            self._sorted_items = sorted(self._collection._collection)
            if self._reverse:
                self._sorted_items = list(reversed(self._sorted_items))

        """
        The __next__() method must return the next item in the sequence. 
        On reaching the end, and in subsequent calls, it must raise StopIteration.
        """
        if self._position >= len(self._sorted_items):
            raise StopIteration()
        value = self._sorted_items[self._position]
        self._position += 1
        return value


class WordCollection(Iterable):
    """
    Concrete Collections provide one or several methods for retrieving fresh
    iterator instances, compatible with the collection class.
    """

    def __init__(self, collection: list[Any] | None = None) -> None:
        self._collection = collection or []

    def __getitem__(self, index: int) -> Any:
        return self._collection[index]

    def __iter__(self) -> AlphabeticalOrderIterator:
        """
        The __iter__() method returns the iterator object itself, by default we
        return the iterator in ascending order.
        """
        return AlphabeticalOrderIterator(self)

    def get_reverse_iterator(self) -> AlphabeticalOrderIterator:
        return AlphabeticalOrderIterator(self, True)

    def add_item(self, item: Any) -> None:
        self._collection.append(item)


if __name__ == "__main__":
    # The client code may or may not know about the Concrete Iterator or
    # Collection classes, depending on the level of indirection you want to know keep
    # in your program.
    collection = WordCollection()
    collection.add_item("B")
    collection.add_item("A")
    collection.add_item("C")

    # 파이썬 반복 구문(for, in, join, list(), tuple() 등)은 iterable 객체를 만나면 __iter__() 호출
    # __iter__()는 AlphabeticalOrderIterator의 __next__() 호출, 값을 하나씩 꺼냄
    print("Straight traversal:")
    print("\n".join(collection))

    print("Reverse traversal:")
    print("\n".join(collection.get_reverse_iterator()), end="")
