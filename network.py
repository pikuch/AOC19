from intcode import Intcode
from collections import deque


class Network:
    def __init__(self, count, code):
        self.nodes = []
        self.queues = []
        for i in range(count):
            node = Intcode()
            node.load(code)
            self.nodes.append(node)
            self.queues.append(deque())
