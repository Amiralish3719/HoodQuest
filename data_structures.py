class Stack:

    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def clear(self):
        self._data = []


class Queue:

    def __init__(self):
        self._data = []
        self._front = 0

    def enqueue(self, item):
        self._data.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        item = self._data[self._front]
        self._front += 1
        if self._front > 64 and self._front * 2 > len(self._data):
            self._data = self._data[self._front:]
            self._front = 0
        return item

    def is_empty(self):
        return self._front >= len(self._data)

    def size(self):
        return len(self._data) - self._front     