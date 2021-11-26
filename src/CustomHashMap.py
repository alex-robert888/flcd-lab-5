import hashlib

class Node:
    def __init__(self, value, next_node):
        self._value = value
        self._nextNode = next_node

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    @property
    def nextNode(self):
        return self._nextNode

    @nextNode.setter
    def nextNode(self, new_value):
        self._nextNode = new_value


class LinkedList:
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    @property
    def size(self):
        return self._size

    def add(self, new_value):
        if self.size == 0:
            new_node = Node(new_value, None)
            self._head = new_node
            self._tail = new_node
            self._size += 1
        else:
            new_node = Node(new_value, None)
            self._tail.nextNode = new_node
            self._tail = new_node
            self._size += 1

        return self.size - 1

    def search(self, value):
        if self.size == 0:
            return None

        current = self._head
        index = 0
        while current is not None:
            if current.value == value:
                return index
            current = current.nextNode
            index += 1

        return None

    def get(self, index):
        if index > self.size - 1:
            return None

        currentIndex = 0
        current = self._head
        while currentIndex < index:
            currentIndex += 1
            current = current.nextNode

        return current.value

    def toList(self):
        if self.size == 0:
            return []

        current = self._head
        list = [current.value]

        while current.nextNode is not None:
            current = current.nextNode
            list.append(current.value)

        return list


class CustomHashMap:
    def __init__(self, capacity):
        if capacity < 1:
            raise Exception("Capacity must be greater than 0")

        self._hashmap = [None] * capacity
        self._capacity = capacity

    @property
    def capacity(self):
        return self._capacity

    def _gethash(self, value):
        if isinstance(value, list):
            listHash = 0
            for element in value:
                listHash += self._gethash(element)
            return listHash % self._capacity
        return int(hashlib.sha1(value.encode("utf-8")).hexdigest(), 16) % self._capacity

    def search(self, value):
        value_hash = self._gethash(value)
        if self._hashmap[value_hash] is None:
            return None

        position = self._hashmap[value_hash].search(value)
        if position is not None:
            return value_hash, position

        return None

    def add(self, value):
        if self.search(value) is not None:
            return None

        value_hash = self._gethash(value)

        if self._hashmap[value_hash] is None:
            self._hashmap[value_hash] = LinkedList()

        list_position = self._hashmap[value_hash].add(value)

        return value_hash, list_position

    def get(self, index):
        if index < self._capacity:
            if self._hashmap[index] is None:
                return None

            return self._hashmap[index].toList()
