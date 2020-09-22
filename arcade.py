from intcode import Intcode


class Arcade:
    def __init__(self):
        self.cpu = Intcode()
        self.screen = {}

    def load_game(self, code):
        self.cpu.load(code)

    def run(self):
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
