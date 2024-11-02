from typing import ( 
    Any, 
    Iterator, 
)


class Stack:
    def __init__(self, stack: list[Any] = []) -> None:
        self.stack = stack

    def is_empty(self) -> bool:
        '''Return True if the list is empty.'''
        return not any(self.stack)
    
    def push(self, value: Any) -> None:
        ''' Adding item to the top of the stack '''
        self.stack.append(value)

    def pop(self) -> Any:
        ''' Extracting an item from the top of the stack '''
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        return self.stack.pop()
    
    def peek(self) -> Any:
        ''' Getting item from the top of the stack without deleting it '''
        if self.is_empty():
            raise IndexError("Peek from an empty stack")
        return self.stack[-1]

    def size(self) -> int:
        ''' Returns the number of items in the stack '''
        return len(self.stack)
    
    def __iter__(self) -> Iterator[Any]:
        ''' Iterator (for item in stack). '''
        return reversed(self.stack)
        
    def __len__(self) -> int:
        ''' Return the number of items in the stack (len(stack)). '''
        return self.size()
    
    def __repr__(self) -> str:
        ''' String representation of the stack (repr(stack)). '''
        return f' --> {repr(self.stack)}'
    
    def __str__(self) -> str:
        ''' String representation for print (print(stack)). '''
        return f' --> {self.stack}'