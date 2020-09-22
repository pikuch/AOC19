from intcode import Intcode


class Arcade:
    def __init__(self):
        self.cpu = Intcode()
        self.screen = {}

    def load_game(self, code):
        self.cpu.load(code)

    def insert_coins(self, n):
        self.cpu.code[0] = 2

    def draw_screen(self):
        tiles = {0: "░░", 1: "██", 2: "▓▓", 3: "==", 4: "()"}
        if (-1, 0) in self.screen:
            score = self.screen[(-1, 0)]
        else:
            score = -1
        print(f"██  {score:60d}  points  ██")
        for row in range(20):
            for col in range(38):
                if (col, row) in self.screen:
                    tile = tiles[self.screen[(col, row)]]
                    print(tile, end="")
            print()

    def auto_move(self):
        for x, y in self.screen.keys():
            if self.screen[(x, y)] == 3:
                paddle = x
            if self.screen[(x, y)] == 4:
                ball = x
        if paddle < ball:
            return "d"
        elif paddle > ball:
            return "a"
        else:
            return "s"

    def run(self, automatic):
        inputs = {"": 0, "a": -1, "s": 0, "d": 1, "j": -1, "k": 0, "l": 1}
        while self.cpu.state != "halted":
            self.cpu.run()
            while len(self.cpu.outputs):
                if len(self.cpu.outputs) >= 3:
                    x = self.cpu.outputs.popleft()
                    y = self.cpu.outputs.popleft()
                    tile = self.cpu.outputs.popleft()
                    self.screen[(x, y)] = tile
                else:
                    print(f"ERROR: Encountered a faulty cpu output: {list(self.cpu.outputs)}")
                    break
            if self.cpu.state != "halted":
                self.draw_screen()
                if not automatic:
                    inp = input("move: ")
                else:
                    inp = self.auto_move()
                self.cpu.add_input(inputs[inp])
