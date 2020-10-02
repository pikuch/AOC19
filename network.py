from intcode import Intcode
from collections import deque


class Network:
    def __init__(self, count, code):
        self.nodes = []
        self.queues = []
        for i in range(count):
            node = Intcode()
            node.load(code)
            node.add_input(i)
            self.nodes.append(node)
            self.queues.append(deque())

    def simulate(self):
        while True:
            for i in range(len(self.nodes)):
                self.nodes[i].step()
                # input
                if self.nodes[i].state == "input_wait":
                    if len(self.queues[i]):
                        x, y = self.queues[i].popleft()
                        self.nodes[i].add_input(x)
                        self.nodes[i].add_input(y)
                    else:
                        self.nodes[i].add_input(-1)
                # output
                if len(self.nodes[i].outputs) >= 3:
                    addr = self.nodes[i].get_output()
                    x = self.nodes[i].get_output()
                    y = self.nodes[i].get_output()
                    print(f"packet from {i} to {addr}: [{x},{y}]")
                    if addr < len(self.nodes):
                        self.queues[addr].append((x, y))
                    else:
                        return addr, x, y

