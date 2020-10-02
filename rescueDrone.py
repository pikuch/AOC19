from intcode import Intcode


class RescueDrone:
    def __init__(self, code):
        self.brain = Intcode()
        self.brain.load(code)
        self.commands = {
            "n": "north",
            "s": "south",
            "e": "east",
            "w": "west",
            "t": "take",
            "d": "drop",
            "i": "inv"
        }

    def act(self, command=""):
        if command != "":
            if command[0] in self.commands:
                command = self.commands[command[0]] + command[1:]
            for c in command:
                self.brain.add_input(ord(c))
            self.brain.add_input(ord("\n"))
        self.brain.run()
        outputs = map(chr, map(int, self.brain.get_all_outputs().split()))
        self.print_output(outputs)

    def print_output(self, outputs):
        for c in outputs:
            print(c, end="")
