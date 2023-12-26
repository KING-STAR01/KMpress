from abc import ABC, abstractmethod


class HuffBaseNode(ABC):

    @abstractmethod
    def is_leaf(self):
        pass

    @abstractmethod
    def weight(self):
        pass


class HuffLeafNode(HuffBaseNode):

    def __init__(self, value: str, weight: int):
        self._value = value
        self._weight = weight
        self._leaf = True

    def value(self):
        return self._value

    def is_leaf(self):
        return self._leaf

    def weight(self):
        return self._weight

    def __str__(self):
        return f"{self._weight}"


class HuffInternalNode(HuffBaseNode):

    def __init__(self, weight: int, leftNode: HuffLeafNode, rightNode: HuffLeafNode):
        self._weight = weight
        self._left = leftNode
        self._right = rightNode
        self._leaf = False

    def is_leaf(self):
        return self._leaf

    def weight(self):
        return self._weight

    def left(self):
        return self._left

    def right(self):
        return self._right

    def __str__(self):
        return f"{self._weight}"


