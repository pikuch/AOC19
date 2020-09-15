
class Intcode:
    def __init__(self):
        self.pc = 0
        self.code = []
        self.inst = {1: self.add,
                     2: self.mul,
                     99: self.halt}
        self.running = False

    def load(self, code):
        self.code = list(map(int, code.split(",")))
        self.pc = 0

    def set(self, setup):
        for pos, val in setup.items():
            self.code[pos] = val

    def run(self):
        self.running = True
        while self.running:
            self.inst[self.code[self.pc]]()

    def halt(self):
        self.running = False

    def add(self):
        self.code[self.code[self.pc + 3]] = self.code[self.code[self.pc + 1]] + self.code[self.code[self.pc + 2]]
        self.pc += 4

    def mul(self):
        self.code[self.code[self.pc + 3]] = self.code[self.code[self.pc + 1]] * self.code[self.code[self.pc + 2]]
        self.pc += 4
