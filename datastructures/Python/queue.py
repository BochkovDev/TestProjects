from typing import ( 
    Any, 
    Iterator, 
)

class Queue:
    def __init__(self):
        self.queue = []

    def is_empty(self) -> bool:
        '''Check if the queue is empty'''
        return len(self.queue) == 0

    def enqueue(self, item) -> None:
        '''Add an element to the end of the queue'''
        self.queue.append(item)

    def dequeue(self) -> Any:
        '''Remove and return the element from the front of the queue'''
        if self.is_empty():
            raise IndexError('Dequeue from an empty queue')
        return self.queue.pop(0)

    def front(self) -> Any:
        '''Return the element at the front of the queue without removing it'''
        if self.is_empty():
            raise IndexError('Front from an empty queue')
        return self.queue[0]

    def size(self) -> int:
        '''Return the number of elements in the queue'''
        return len(self.queue)
    
    def __len__(self) -> int:
        '''Enable len() to return the size of the queue'''
        return self.size()

    def __str__(self) -> str:
        '''Return a string representation of the queue'''
        return f"Queue({self.queue})"

    def __repr__(self) -> str:
        '''Return a more detailed string representation for developers'''
        return f"Queue({self.queue})"

    def __iter__(self) -> Iterator:
        '''Make the queue iterable (support for for-loop)'''
        return iter(self.queue)

    def __eq__(self, other) -> bool:
        '''Check if two queues are equal by comparing their elements'''
        if isinstance(other, Queue):
            return self.queue == other.queue
        return False
    


from .doubly_linked_list import DoublyLinkedList

class Queue:
    def __init__(self):
        self.queue = DoublyLinkedList()

    def is_empty(self) -> bool:
        '''Check if the queue is empty'''
        return self.queue.head is None

    def enqueue(self, item) -> None:
        '''Add an element to the end of the queue'''
        self.queue.append(item) 

    def dequeue(self) -> Any:
        '''Remove and return the element from the front of the queue'''
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        value = self.queue.head.data
        if self.queue.head == self.queue.tail: 
            self.queue.head = self.queue.tail = None
        else:
            self.queue.head = self.queue.head.next
            self.queue.head.prev = None
        return value

    def front(self) -> Any:
        '''Return the element at the front of the queue without removing it'''
        if self.is_empty():
            raise IndexError("Front from an empty queue")
        return self.queue.head.data

    def size(self) -> int:
        '''Return the number of elements in the queue'''
        current = self.queue.head
        count = 0
        while current:
            count += 1
            current = current.next
        return count

    def __len__(self) -> int:
        '''Enable len() to return the size of the queue'''
        return self.size()

    def __str__(self) -> str:
        '''Return a string representation of the queue'''
        return str(self.queue)

    def __repr__(self) -> str:
        '''Return a more detailed string representation for developers'''
        return self.__str__()

    def __iter__(self) -> Iterator:
        '''Make the queue iterable (support for for-loop)'''
        current = self.queue.head
        while current:
            yield current.data
            current = current.next

    def __eq__(self, other) -> bool:
        '''Check if two queues are equal by comparing their elements'''
        if isinstance(other, Queue):
            return list(self) == list(other)
        return False