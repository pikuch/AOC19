from intcode import Intcode


class EmHuPaR:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dir = 0  # up
        self.brain = None

    def load(self, program):
        self.brain = Intcode()
        self.brain.load(program)
        self.brain.exit_on_output = True

    def run(self, panels):
        dx = {0: 0, 1: 1, 2: 0, 3: -1}
        dy = {0: -1, 1: 0, 2: 1, 3: 0}
        while True:
            self.brain.set_input(panels[(self.x, self.y)])
            self.brain.run()
            if self.brain.state == "halted":
                return
            color = self.brain.get_output()
            self.brain.run()
            turn = self.brain.get_output()
            panels[(self.x, self.y)] = color
            if turn == 1:
                self.dir = (self.dir + 1) % 4
            else:
                self.dir = (self.dir + 3) % 4
            self.x += dx[self.dir]
            self.y += dy[self.dir]
