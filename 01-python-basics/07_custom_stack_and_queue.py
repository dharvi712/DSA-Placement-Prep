"""
Problem   : Design a Custom Stack (+ Queue variant)
Topic     : Python Basics for DSA
Difficulty: Easy
Date      : 2026-08-01

Approach (Stack):
    Use a plain Python list, operating ONLY on its END for both push
    and pop (via append/pop). The end of a list is O(1) for add/remove
    because nothing needs to shift. The front would be O(n) (insert(0,x)
    or pop(0)), since every other element would have to shift to make
    room / close the gap. Since a stack is LIFO (Last In, First Out),
    operating on the same end for both push and pop is exactly what
    gives LIFO behavior "for free."

Approach (Queue):
    A queue is FIFO (First In, First Out) - items must be added at one
    end and removed from the OTHER end. Switch the underlying container
    to a deque (not a list), because removing from the front of a list
    is O(n), but deque.popleft() is O(1). push (append, adds to back)
    stays the same; pop is changed from .pop() (removes from back) to
    .popleft() (removes from front), so the earliest-added item comes
    out first.

Time Complexity : Stack -> push/pop/peek/is_empty all O(1) (amortized for push)
                  Queue -> push/pop/peek/is_empty all O(1)
Space Complexity: O(n) -> where n = number of items currently stored
"""

from collections import deque


class Stack:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)  # O(1) amortized - adds to the end

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()  # O(1) - removes from the end

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]  # O(1) - direct index access

    def is_empty(self):
        return len(self.items) == 0  # O(1) - len() reads a stored counter


class Queue:
    def __init__(self):
        self.items = deque()

    def push(self, x):
        self.items.append(x)  # O(1) - adds to the back

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty queue")
        return self.items.popleft()  # O(1) - removes from the front

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self.items[0]  # O(1) on a deque

    def is_empty(self):
        return len(self.items) == 0  # O(1)


if __name__ == "__main__":
    # --- Stack tests (LIFO) ---
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    print("Stack pop order (expect 3,2,1):", s.pop(), s.pop(), s.pop())
    print("Stack is_empty after popping all (expect True):", s.is_empty())

    try:
        s.pop()
        print("Test FAIL: expected IndexError on empty stack pop")
    except IndexError:
        print("Test PASS: empty stack pop raises IndexError as expected")

    # --- Queue tests (FIFO) ---
    q = Queue()
    q.push(1)
    q.push(2)
    q.push(3)
    print("Queue pop order (expect 1,2,3):", q.pop(), q.pop(), q.pop())
    print("Queue is_empty after popping all (expect True):", q.is_empty())
