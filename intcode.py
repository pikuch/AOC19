from collections import deque


class Intcode:
    def __init__(self):
        self.pc = 0
        self.code = []
        self.rb = 0
        self.inputs = deque()
        self.outputs = deque()
        self.inst = {"01": self.add,
                     "02": self.mul,
                     "03": self.inp,
                     "04": self.outp,
                     "05": self.jit,
                     "06": self.jif,
                     "07": self.lt,
                     "08": self.eq,
                     "09": self.arb,
                     "99": self.halt}
        self.inst_length = {"01": 4, "02": 4, "03": 2, "04": 2, "05": 3, "06": 3, "07": 4, "08": 4, "09": 2, "99": 1}
        self.state = "fresh"
        self.exit_on_output = False
        self.memory_allocations = 0

    def get_asm(self):
        lines = []
        i = 0
        while i < len(self.code):
            current_inst = self.code[i]
            line = f"{i:3d}-{i + self.inst_length[self.code[i]] - 1:3d}    {self.inst[self.code[i]].__name__}\t" + \
                          " ".join(map(str, self.code[i+1:i+self.inst_length[self.code[i]]]))
            i += self.inst_length[self.code[i]]
            lines.append(line)
            if current_inst == 99:
                lines.append(f"{i:3d}-{len(self.code)-1:3d}    " + " ".join(map(str, self.code[i:])))
                break
        return "\n".join(lines)

    def load(self, code):
        self.code = list(map(int, code.split(",")))
        self.inputs.clear()
        self.outputs.clear()
        self.rb = 0
        self.pc = 0
        self.state = "loaded"

    def set_input(self, value):
        self.inputs.clear()
        self.inputs.append(value)

    def add_input(self, value):
        self.inputs.append(value)

    def get_output(self):
        return self.outputs.popleft()

    def get_all_outputs(self):
        outp = " ".join(map(str, self.outputs))
        self.outputs.clear()
        return outp

    def decode(self, code):
        s = f"{code:05d}"
        return s[-2:], s[2::-1]

    def get_addr(self, address, mode):
        if mode == "0":  # position mode
            return self.code[address]
        elif mode == "1":  # immediate mode
            return address
        else:  # relative mode
            return self.rb + self.code[address]

    def run(self):
        self.state = "running"
        while self.state == "running":
            try:
                instruction, modes = self.decode(self.code[self.pc])
                self.inst[instruction](modes)
            except IndexError:
                self.code.extend([0]*1000)
                self.memory_allocations += 1

    def halt(self, modes):
        self.state = "halted"

    def inp(self, modes):
        if len(self.inputs):
            self.code[self.get_addr(self.pc + 1, modes[0])] = self.inputs.popleft()
            self.pc += 2
        else:
            self.state = "input_wait"

    def outp(self, modes):
        self.outputs.append(self.code[self.get_addr(self.pc + 1, modes[0])])
        self.pc += 2
        if self.exit_on_output:
            self.state = "output"

    def add(self, modes):
        self.code[self.get_addr(self.pc + 3, modes[2])] = self.code[self.get_addr(self.pc + 1, modes[0])] +\
                                                          self.code[self.get_addr(self.pc + 2, modes[1])]
        self.pc += 4

    def mul(self, modes):
        self.code[self.get_addr(self.pc + 3, modes[2])] = self.code[self.get_addr(self.pc + 1, modes[0])] *\
                                                          self.code[self.get_addr(self.pc + 2, modes[1])]
        self.pc += 4

    def jit(self, modes):
        if self.code[self.get_addr(self.pc + 1, modes[0])] != 0:
            self.pc = self.code[self.get_addr(self.pc + 2, modes[1])]
        else:
            self.pc += 3

    def jif(self, modes):
        if self.code[self.get_addr(self.pc + 1, modes[0])] == 0:
            self.pc = self.code[self.get_addr(self.pc + 2, modes[1])]
        else:
            self.pc += 3

    def lt(self, modes):
        if self.code[self.get_addr(self.pc + 1, modes[0])] < self.code[self.get_addr(self.pc + 2, modes[1])]:
            self.code[self.get_addr(self.pc + 3, modes[2])] = 1
        else:
            self.code[self.get_addr(self.pc + 3, modes[2])] = 0
        self.pc += 4

    def eq(self, modes):
        if self.code[self.get_addr(self.pc + 1, modes[0])] == self.code[self.get_addr(self.pc + 2, modes[1])]:
            self.code[self.get_addr(self.pc + 3, modes[2])] = 1
        else:
            self.code[self.get_addr(self.pc + 3, modes[2])] = 0
        self.pc += 4

    def arb(self, modes):
        self.rb += self.code[self.get_addr(self.pc + 1, modes[0])]
        self.pc += 2
