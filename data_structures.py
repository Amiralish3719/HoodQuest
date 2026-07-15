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



class MaxHeap:

    def __init__(self):
        self._data = []              
        self._index_of = {}         
    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]
        self._index_of[self._data[i][1]] = i
        self._index_of[self._data[j][1]] = j

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._data[i][0] > self._data[parent][0]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self._data)
        while True:
            left, right, largest = 2 * i + 1, 2 * i + 2, i
            if left < n and self._data[left][0] > self._data[largest][0]:
                largest = left
            if right < n and self._data[right][0] > self._data[largest][0]:
                largest = right
            if largest == i:
                break
            self._swap(i, largest)
            i = largest

    def insert(self, score, username):
        if username in self._index_of:
            self.update_score(username, score)
            return
        self._data.append((score, username))
        idx = len(self._data) - 1
        self._index_of[username] = idx
        self._sift_up(idx)

    def update_score(self, username, new_score):
        if username not in self._index_of:
            self.insert(new_score, username)
            return
        idx = self._index_of[username]
        old_score = self._data[idx][0]
        self._data[idx] = (new_score, username)
        if new_score > old_score:
            self._sift_up(idx)
        elif new_score < old_score:
            self._sift_down(idx)

    def peek_max(self):
        if self.is_empty():
            return None
        return self._data[0]

    def extract_max(self):
        if self.is_empty():
            return None
        top = self._data[0]
        last = self._data.pop()
        del self._index_of[top[1]]
        if self._data:
            self._data[0] = last
            self._index_of[last[1]] = 0
            self._sift_down(0)
        return top

    def top_n(self, n):
        temp_data = list(self._data)
        temp_index = dict(self._index_of)
        result = []
        clone = MaxHeap()
        clone._data = list(self._data)
        clone._index_of = dict(self._index_of)
        count = min(n, clone.size())
        for _ in range(count):
            result.append(clone.extract_max())
        return result


class _BSTNode:
    __slots__ = ("key", "value", "left", "right")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class BST:


    def __init__(self):
        self._root = None
        self._count = 0

    def is_empty(self):
        return self._root is None

    def insert(self, key, value):
        if self._root is None:
            self._root = _BSTNode(key, value)
            self._count += 1
            return
        node = self._root
        while True:
            if key == node.key:
                node.value = value
                return
            elif key < node.key:
                if node.left is None:
                    node.left = _BSTNode(key, value)
                    self._count += 1
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = _BSTNode(key, value)
                    self._count += 1
                    return
                node = node.right

    def search(self, key):
        node = self._root
        while node is not None:
            if key == node.key:
                return node.value
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def update(self, key, value):
        self.insert(key, value)

    def delete(self, key):
        def _delete(node, key):
            if node is None:
                return None
            if key < node.key:
                node.left = _delete(node.left, key)
            elif key > node.key:
                node.right = _delete(node.right, key)
            else:
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                successor = node.right
                while successor.left is not None:
                    successor = successor.left
                node.key, node.value = successor.key, successor.value
                node.right = _delete(node.right, successor.key)
            return node

        self._root = _delete(self._root, key)

    def inorder(self):
        result = []

        def _walk(node):
            if node is None:
                return
            _walk(node.left)
            result.append((node.key, node.value))
            _walk(node.right)

        _walk(self._root)
        return result

    def __len__(self):
        return self._count
