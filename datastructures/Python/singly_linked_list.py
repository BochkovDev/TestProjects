from dataclasses import dataclass
from typing import ( 
    Any, 
    Optional, 
    Iterable,
    Iterator, 
    Union,
    overload,
)


@dataclass
class Node:
    data: Any
    next: Optional['Node'] = None

class SinglyLinkedList:
    head: Optional[Node]

    def __init__(self, head: Optional[Node] = None) -> None:
        self.head = head

    def append(self, data: Any) -> None:
        ''' Append node to the end of the list. '''
        new_node = Node(data=data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def prepend(self, data: Any) -> None:
        ''' Append node to the top of the list. '''
        self.head = Node(data=data, next=self.head)

    def insert(self, index: int, data: Any) -> None:
        ''' Insert node by index. '''
        if index < 0:
            raise IndexError('Index cannot be negative')
        if index == 0:
            self.prepend(data)
            return
        
        current = self._get_node_at(index - 1)
        new_node = Node(data=data, next=current.next)
        current.next = new_node

    def extend(self, iterable: Iterable[Any]) -> None:
        ''' Append elements from an iterable to the end of the list. '''
        iterator = iter(iterable)
        first_item = next(iterator, None)

        if first_item is None:
            return
        
        if not self.head:
            self.head = Node(data=first_item)
            current = self.head
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = Node(data=first_item)
            current = current.next

        for item in iterator:
            current.next = Node(data=item)
            current = current.next

    def delete(self, data: Any) -> None:
        ''' Delete the first node with the value. '''
        if not self.head:
            return
        
        if self.head.data == data:
            self.head = self.head.next
            return

        current = self.head
        while current.next and current.next.data != data:
            current = current.next

        if current.next:
            current.next = current.next.next

    def delete_at(self, index: int) -> None:
        ''' Delete node by index. '''
        if index < 0:
            raise IndexError('Index cannot be negative')

        if not self.head:
            raise IndexError('List is empty')
        
        if index == 0:
            self.head = self.head.next
            return

        current = self._get_node_at(index - 1)
        if not current.next:
            raise IndexError('Index out of range')
        current.next = current.next.next

    def remove_duplicates(self) -> None:
        ''' Remove duplicates from the list. '''
        if not self.head:
            return

        seen = set()
        current = self.head
        seen.add(current.data)

        while current.next:
            if current.next.data in seen:
                current.next = current.next.next
            else:
                seen.add(current.next.data)
                current = current.next

    def clear(self) -> None:
        ''' Clear all nodes. '''
        self.head = None

    def find(self, data: Any) -> Optional[int]:
        ''' Find index of data. '''
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return None

    def reverse(self) -> None:
        ''' Reverse the list. '''
        previous = None
        current = self.head

        while current:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        self.head = previous

    def is_empty(self) -> bool:
        ''' Return True if the list is empty. '''
        return self.head is None

    def _get_node_at(self, index: int) -> Node:
        ''' Helper method to retrieve node by index. '''
        if index < 0:
            raise IndexError('Index cannot be negative')

        current = self.head
        for _ in range(index):
            if not current:
                raise IndexError('Index out of range')
            current = current.next

        if not current:
            raise IndexError('Index out of range')
        
        return current

    @overload
    def __getitem__(self, index: int) -> Any: ...

    @overload
    def __getitem__(self, index: slice) -> 'SinglyLinkedList': ...

    def __getitem__(self, index: Union[int, slice]) -> Union[Any, 'SinglyLinkedList']:
        ''' Get data by index (list[index]). '''
        if isinstance(index, slice):
            sliced_list = SinglyLinkedList()
            current = self.head

            start = index.start if index.start is not None else 0
            stop = index.stop if index.stop is not None else len(self)
            step = index.step if index.step is not None else 1

            for _ in range(start):
                if not current:
                    return sliced_list
                current = current.next
            
            for i in range(start, stop, step):
                if not current:
                    break
                sliced_list.append(current.data)
                for _ in range(step):
                    if not current:
                        break
                    current = current.next
            return sliced_list
        return self._get_node_at(index).data

    def __setitem__(self, index: int, value: Any) -> None:
        ''' Set data by index (list[index] = value). '''
        self._get_node_at(index).data = value

    def __delitem__(self, index: int) -> None:
        ''' Delete node by index (del list[index]). '''
        self.delete_at(index)

    def __add__(self, other: 'SinglyLinkedList') -> 'SinglyLinkedList':
        ''' Concatenate two lists (list1 + list2) '''
        new_list = SinglyLinkedList()

        iterator_self = iter(self)
        first_item = next(iterator_self, None)
        if first_item is not None:
            new_list.head = Node(data=first_item)
            current = new_list.head

            for item in iterator_self:
                current.next = Node(data=item)
                current = current.next
        else:
            current = None

        iterator_other = iter(other)
        first_item = next(iterator_other, None)
        if first_item is not None:
            if not current:
                new_list.head = Node(data=first_item)
                current = new_list.head
            else:
                current.next = Node(data=first_item)
                current = current.next
                for item in iterator_other:
                    current.next = Node(data=item)
                    current = current.next

        return new_list

    def __bool__(self) -> bool:
        ''' Check if the list is not empty (bool(list)). '''
        return self.head is not None

    def __contains__(self, value: Any) -> bool:
        ''' Check if value exists in the list. '''
        return self.find(value) is not None

    def __eq__(self, other: 'SinglyLinkedList') -> bool:
        if not isinstance(other, SinglyLinkedList):
            return False
        
        current_self = self.head
        current_other = other.head
        
        while current_self and current_other:
            if current_self.data != current_other.data:
                return False
            current_self = current_self.next
            current_other = current_other.next
        
        return current_self is None and current_other is None

    def __iter__(self) -> Iterator[Any]:
        ''' Iterator (for item in list). '''
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __len__(self) -> int:
        ''' Get the length of the list (len(list)). '''
        length = 0
        current = self.head
        while current:
            length += 1
            current = current.next
        return length

    def __reversed__(self) -> Iterator[Any]:
        ''' Reverse iterator (for item in reversed(list)). '''
        reversed_list = []
        current = self.head
        while current:
            reversed_list.insert(0, current.data)
            current = current.next
        return iter(reversed_list)

    def __repr__(self) -> str:
        ''' String representation of the list (repr(list)). '''
        return repr(list(self))

    def __str__(self) -> str:
        ''' String representation for print (print(list)). '''
        return str(list(self))