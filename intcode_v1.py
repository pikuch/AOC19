from collections import deque


class Intcode:
    def __init__(self):
        self.pc = 0
        self.code = []
        self.rb = 0
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
                     5: self.jit_pp,
                     105: self.jit_ip,
                     1005: self.jit_pi,
                     1105: self.jit_ii,
                     6: self.jif_pp,
                     106: self.jif_ip,
                     1006: self.jif_pi,
                     1106: self.jif_ii,
                     7: self.lt_pp,
                     107: self.lt_ip,
                     1007: self.lt_pi,
                     1107: self.lt_ii,
                     8: self.eq_pp,
                     108: self.eq_ip,
                     1008: self.eq_pi,
                     1108: self.eq_ii,
                     9: self.arb_p,
                     109: self.arb_i,
                     209: self.arb_r,
                     99: self.halt}
        self.inst_length = {1: 4, 101: 4, 1001: 4, 1101: 4,
                            2: 4, 102: 4, 1002: 4, 1102: 4,
                            3: 2, 4: 2, 104: 2,
                            5: 3, 105: 3, 1005: 3, 1105: 3,
                            6: 3, 106: 3, 1006: 3, 1106: 3,
                            7: 4, 107: 4, 1007: 4, 1107: 4,
                            8: 4, 108: 4, 1008: 4, 1108: 4,
                            9: 2, 109: 2, 209: 2,
                            99: 1}
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

    def set(self, setup):
        for pos, val in setup.items():
            self.code[pos] = val

    def run(self):
        self.state = "running"
        while self.state == "running":
            try:
                self.inst[self.code[self.pc]]()
            except IndexError:
                self.code.extend([0]*1000)
                self.memory_allocations += 1

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
        if self.exit_on_output:
            self.state = "output"

    def outp_i(self):
        self.outputs.append(self.code[self.pc + 1])
        self.pc += 2
        if self.exit_on_output:
            self.state = "output"

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

    def jit_pp(self):
        if self.code[self.code[self.pc + 1]] != 0:
            self.pc = self.code[self.code[self.pc + 2]]
        else:
            self.pc += 3

    def jit_ip(self):
        if self.code[self.pc + 1] != 0:
            self.pc = self.code[self.code[self.pc + 2]]
        else:
            self.pc += 3

    def jit_pi(self):
        if self.code[self.code[self.pc + 1]] != 0:
            self.pc = self.code[self.pc + 2]
        else:
            self.pc += 3

    def jit_ii(self):
        if self.code[self.pc + 1] != 0:
            self.pc = self.code[self.pc + 2]
        else:
            self.pc += 3

    def jif_pp(self):
        if self.code[self.code[self.pc + 1]] == 0:
            self.pc = self.code[self.code[self.pc + 2]]
        else:
            self.pc += 3

    def jif_ip(self):
        if self.code[self.pc + 1] == 0:
            self.pc = self.code[self.code[self.pc + 2]]
        else:
            self.pc += 3

    def jif_pi(self):
        if self.code[self.code[self.pc + 1]] == 0:
            self.pc = self.code[self.pc + 2]
        else:
            self.pc += 3

    def jif_ii(self):
        if self.code[self.pc + 1] == 0:
            self.pc = self.code[self.pc + 2]
        else:
            self.pc += 3

    def lt_pp(self):
        if self.code[self.code[self.pc + 1]] < self.code[self.code[self.pc + 2]]:
            self.code[self.code[self.pc + 3]] = 1
        else:
            self.code[self.code[self.pc + 3]] = 0
        self.pc += 4

    def lt_ip(self):
        if self.code[self.pc + 1] < self.code[self.code[self.pc + 2]]:
            self.code[self.code[self.pc + 3]] = 1
        else:
            self.code[self.code[self.pc + 3]] = 0
        self.pc += 4

    def lt_pi(self):
        if self.code[self.code[self.pc + 1]] < self.code[self.pc + 2]:
            self.code[self.code[self.pc + 3]] = 1
        else:
            self.code[self.code[self.pc + 3]] = 0
        self.pc += 4

    def lt_ii(self):
        if self.code[self.pc + 1] < self.code[self.pc + 2]:
            self.code[self.code[self.pc + 3]] = 1
        else:
            self.code[self.code[self.pc + 3]] = 0
        self.pc += 4

    def eq_pp(self):
        if self.code[self.code[self.pc + 1]] == self.code[self.code[self.pc + 2]]:
            self.code[self.code[self.pc + 3]] = 1
        else:
            self.code[self.code[self.pc + 3]] = 0
        self.pc += 4

    def eq_ip(self):
        if self.code[self.pc + 1] == self.code[self.code[self.pc + 2]]:
            self.code[self.code[self.pc + 3]] = 1
        else:
            self.code[self.code[self.pc + 3]] = 0
        self.pc += 4

    def eq_pi(self):
        if self.code[self.code[self.pc + 1]] == self.code[self.pc + 2]:
            self.code[self.code[self.pc + 3]] = 1
        else:
            self.code[self.code[self.pc + 3]] = 0
        self.pc += 4

    def eq_ii(self):
        if self.code[self.pc + 1] == self.code[self.pc + 2]:
            self.code[self.code[self.pc + 3]] = 1
        else:
            self.code[self.code[self.pc + 3]] = 0
        self.pc += 4

    def arb_p(self):
        self.rb += self.code[self.code[self.pc + 1]]
        self.pc += 2

    def arb_i(self):
        self.rb += self.code[self.pc + 1]
        self.pc += 2

    def arb_r(self):
        self.rb += self.code[self.rb + self.code[self.pc + 1]]
        self.pc += 2
