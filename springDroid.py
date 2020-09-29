from intcode import Intcode


class SpringDroid:
    def __init__(self, data):
        self.brain = Intcode()
        self.brain.load(data)

    def walk(self, code):
        for line in code:
            for char in line:
                self.brain.add_input(ord(char))
            self.brain.add_input(ord("\n"))
        for c in "WALK":
            self.brain.add_input(ord(c))
        self.brain.add_input(ord("\n"))

        self.brain.run()
        output = list(map(int, self.brain.get_all_outputs().split()))
        return output

    def run(self, code):
        for line in code:
            for char in line:
                self.brain.add_input(ord(char))
            self.brain.add_input(ord("\n"))
        for c in "RUN":
            self.brain.add_input(ord(c))
        self.brain.add_input(ord("\n"))

        self.brain.run()
        output = list(map(int, self.brain.get_all_outputs().split()))
        return output
