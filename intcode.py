from collections import deque


class Intcode:
    def __init__(self):
        self.pc = 0
        self.code = []
        self.inputs = deque()
        self.outputs = deque()
        self.inst = {1: self.add_pp,
                     101: self.add_ip,
                     1001: self.add_pi,
                     1101: self.add_ii,
                     2: self.mul_pp,
                     102: self.mul_ip,
                     1002: self.mul_pi,
                     1102: self.mul_ii,
                     3: self.inp_p,
                     4: self.outp_p,
                     104: self.outp_i,
                     99: self.halt}
        self.state = ""

    def load(self, code):
        self.code = list(map(int, code.split(",")))
        self.pc = 0

    def set(self, setup):
        for pos, val in setup.items():
            self.code[pos] = val

    def run(self):
        self.state = "running"
        while self.state == "running":
            self.inst[self.code[self.pc]]()

    def halt(self):
        self.state = "halted"

    def inp_p(self):
        if len(self.inputs):
            self.code[self.code[self.pc + 1]] = self.inputs.popleft()
            self.pc += 2
        else:
            self.state = "input_wait"

    def outp_p(self):
        self.outputs.append(self.code[self.code[self.pc + 1]])
        self.pc += 2

    def outp_i(self):
        self.outputs.append(self.code[self.pc + 1])
        self.pc += 2

    def add_pp(self):
        self.code[self.code[self.pc + 3]] = self.code[self.code[self.pc + 1]] + self.code[self.code[self.pc + 2]]
        self.pc += 4

    def add_ip(self):
        self.code[self.code[self.pc + 3]] = self.code[self.pc + 1] + self.code[self.code[self.pc + 2]]
        self.pc += 4

    def add_pi(self):
        self.code[self.code[self.pc + 3]] = self.code[self.code[self.pc + 1]] + self.code[self.pc + 2]
        self.pc += 4

    def add_ii(self):
        self.code[self.code[self.pc + 3]] = self.code[self.pc + 1] + self.code[self.pc + 2]
        self.pc += 4

    def mul_pp(self):
        self.code[self.code[self.pc + 3]] = self.code[self.code[self.pc + 1]] * self.code[self.code[self.pc + 2]]
        self.pc += 4

    def mul_ip(self):
        self.code[self.code[self.pc + 3]] = self.code[self.pc + 1] * self.code[self.code[self.pc + 2]]
        self.pc += 4

    def mul_pi(self):
        self.code[self.code[self.pc + 3]] = self.code[self.code[self.pc + 1]] * self.code[self.pc + 2]
        self.pc += 4

    def mul_ii(self):
        self.code[self.code[self.pc + 3]] = self.code[self.pc + 1] * self.code[self.pc + 2]
        self.pc += 4
