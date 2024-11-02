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
    prev: Optional['Node'] = None
    next: Optional['Node'] = None

class DoublyLinkedList:
    head: Optional[Node]
    tail: Optional[Node]

    def __init__(self, head: Optional[Node] = None, tail: Optional[Node] = None) -> None:
        self.head = head
        self.tail = tail

    def append(self, data: Any) -> None:
        '''Append node to the end of the list.'''
        new_node = Node(data=data)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def prepend(self, data: Any) -> None:
        '''Append node to the top of the list.'''
        new_node = Node(data=data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.head.prev = new_node
            new_node.next = self.head
            self.head = new_node

    def insert(self, index: int, data: Any) -> None:
        '''Insert node by index.'''
        if index < 0:
            raise IndexError('Index cannot be negative')
        if index == 0:
            self.prepend(data)
            return
        
        new_node = Node(data=data)
        current = self._get_node_at(index - 1)
        next_node = current.next
        
        new_node.next = next_node
        new_node.prev = current
        
        current.next = new_node
        if next_node:
            next_node.prev = new_node
        else:
            self.tail = new_node

    def extend(self, iterable: Iterable[Any]) -> None:
        '''Append elements from an iterable to the end of the list.'''
        for item in iterable:
            self.append(item)

    def delete(self, data: Any) -> None:
        '''Delete the first node with the value.'''
        current = self.head

        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                return
            current = current.next

    def delete_at(self, index: int) -> None:
        '''Delete node by index.'''
        if index < 0:
            raise IndexError('Index cannot be negative')
        current = self._get_node_at(index)
        
        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next

        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev

    def remove_duplicates(self) -> None:
        '''Remove duplicates from the list.'''
        if not self.head:
            return

        seen = set()
        current = self.head
        while current:
            if current.data in seen:
                next_node = current.next
                if current.prev:
                    current.prev.next = next_node
                if next_node:
                    next_node.prev = current.prev
                else:
                    self.tail = current.prev
            else:
                seen.add(current.data)
            current = current.next

    def clear(self) -> None:
        '''Clear all nodes.'''
        self.head = None
        self.tail = None

    def find(self, data: Any) -> Optional[int]:
        '''Find index of data.'''
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return None
    
    def reverse(self) -> None:
        '''Reverse the list.'''
        current = self.head
        prev_node = None

        while current:
            next_node = current.next
            current.next = prev_node
            current.prev = next_node
            prev_node = current
            current = next_node

        self.head, self.tail = self.tail, self.head

    def is_empty(self) -> bool:
        '''Return True if the list is empty.'''
        return self.head is None

    def _get_node_at(self, index: int) -> Node:
        '''Helper method to retrieve node by index.'''
        if index < 0:
            raise IndexError('Index cannot be negative')

        current = self.head
        for _ in range(index):
            if not current:
                raise IndexError('Index out of range')
            current = current.next

        if current is None:
            raise IndexError('Index out of range')

        return current
    
    @overload
    def __getitem__(self, index: int) -> Any: ...

    @overload
    def __getitem__(self, index: slice) -> 'DoublyLinkedList': ...

    def __getitem__(self, index: Union[int, slice]) -> Union[Any, 'DoublyLinkedList']:
        '''Get data by index (list[index]).'''
        if isinstance(index, slice):
            sliced_list = DoublyLinkedList()
            current = self.head

            start = index.start if index.start is not None else 0
            stop = index.stop if index.stop is not None else len(self)
            step = index.step if index.step is not None else 1

            for _ in range(start):
                if current is None:
                    return sliced_list
                current = current.next
            
            for i in range(start, stop, step):
                if current is None:
                    break
                sliced_list.append(current.data)
                for _ in range(step):
                    if current is None:
                        break
                    current = current.next
            return sliced_list
        return self._get_node_at(index).data
    
    def __setitem__(self, index: int, value: Any) -> None:
        '''Set data by index (list[index] = value).'''
        self._get_node_at(index).data = value

    def __delitem__(self, index: int) -> None:
        '''Delete node by index (del list[index]).'''
        self.delete_at(index)

    def __add__(self, other: 'DoublyLinkedList') -> 'DoublyLinkedList':
        '''Concatenate two lists (list1 + list2).'''
        new_list = DoublyLinkedList()
        for item in self:
            new_list.append(item)
        for item in other:
            new_list.append(item)
        return new_list
    
    def __bool__(self) -> bool:
        '''Check if the list is not empty (bool(list)).'''
        return self.head is not None
    
    def __contains__(self, value: Any) -> bool:
        '''Check if the list contains a value (value in list).'''
        current = self.head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False
    
    def __eq__(self, other: 'DoublyLinkedList') -> bool:
        ''' Check if two lists are equal (list1 == list2). '''
        if not isinstance(other, DoublyLinkedList):
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
        ''' Return the number of elements in the list (len(list)). '''
        length = 0
        current = self.head
        while current:
            length += 1
            current = current.next
        return length
    
    def __reversed__(self) -> Iterator[Any]:
        ''' Iterator for backward traversal (for item in reversed(list)). '''
        current = self.tail
        while current:
            yield current.data
            current = current.prev

    def __repr__(self) -> str:
        ''' String representation of the list (repr(list)). '''
        return repr(list(self))

    def __str__(self) -> str:
        ''' String representation for print (print(list)). '''
        return str(list(self))