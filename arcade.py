from intcode import Intcode


class Arcade:
    def __init__(self):
        self.cpu = Intcode()
        self.screen = {}

    def load_game(self, code):
        self.cpu.load(code)

    def draw_screen(self):
        tiles = {0: "░░", 1: "██", 2: "▓▓", 3: "==", 4: "()"}
        for row in range(20):
            for col in range(40):
                if (col, row) in self.screen:
                    tile = tiles[self.screen[(col, row)]]
                    print(tile, end="")
            print()


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
