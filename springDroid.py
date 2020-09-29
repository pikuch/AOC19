from intcode import Intcode


class SpringDroid:
    def __init__(self, data):
        self.brain = Intcode()
        self.brain.load(data)

    def run(self, code):
        for c in code:
            self.brain.add_input(ord(c))
        self.brain.add_input(ord("\n"))
        for c in "WALK":
            self.brain.add_input(ord(c))
        self.brain.add_input(ord("\n"))
        self.brain.run()
        output = map(chr, map(int, self.brain.get_all_outputs().split()))
        return output
