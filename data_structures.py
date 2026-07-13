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
    

class _HTNode:
    __slots__ = ("key", "value", "next")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:

    def __init__(self, capacity=16):
        self._capacity = capacity
        self._buckets = [None] * self._capacity
        self._count = 0

    def _hash(self, key):
        h = 0
        for ch in str(key):
            h = (h * 31 + ord(ch)) & 0xFFFFFFFF
        return h % self._capacity

    def _resize(self, new_capacity):
        old_items = list(self.items())
        self._capacity = new_capacity
        self._buckets = [None] * self._capacity
        self._count = 0
        for k, v in old_items:
            self.put(k, v)

    def put(self, key, value):
        idx = self._hash(key)
        node = self._buckets[idx]
        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next
        new_node = _HTNode(key, value)
        new_node.next = self._buckets[idx]
        self._buckets[idx] = new_node
        self._count += 1
        if self._count / self._capacity > 0.75:
            self._resize(self._capacity * 2)

    def get(self, key, default=None):
        idx = self._hash(key)
        node = self._buckets[idx]
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        return default

    def contains(self, key):
        idx = self._hash(key)
        node = self._buckets[idx]
        while node is not None:
            if node.key == key:
                return True
            node = node.next
        return False

    def remove(self, key):
        idx = self._hash(key)
        node = self._buckets[idx]
        prev = None
        while node is not None:
            if node.key == key:
                if prev is None:
                    self._buckets[idx] = node.next
                else:
                    prev.next = node.next
                self._count -= 1
                return True
            prev = node
            node = node.next
        return False

    def items(self):
        result = []
        for idx in range(self._capacity):
            node = self._buckets[idx]
            while node is not None:
                result.append((node.key, node.value))
                node = node.next
        return result

    def __len__(self):
        return self._count
