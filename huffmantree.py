from huffmands import HuffLeafNode, HuffInternalNode


class HuffTree:

    def __init__(self, *args):
        if len(args) == 3:
            self.root = HuffInternalNode(args[0], args[1], args[2])
        else:
            self.root = HuffLeafNode(args[0], args[1])

    def weight(self):
        return self.root.weight()

    def __lt__(self, other):
        return self.root.weight() < other.root.weight() if self.root.weight() != other.root.weight() else -1

    def __str__(self):
        return str(self.root.weight())

    def __repr__(self):
        return str(self.root.weight())
