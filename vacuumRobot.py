from intcode import Intcode


class VacuumRobot:
    def __init__(self):
        self.brain = Intcode()

    def load(self, code):
        self.brain.load(code)

    def grab_camera(self):
        self.brain.run()
        return "".join(map(chr, map(int, self.brain.get_all_outputs().split())))

    def run_path(self, order, subpaths):
        self.brain.code[0] = 2  # switch to the path following mode
        line = list(map(ord, ",".join(map(str, order)) + "\n"))
        for c in line:
            self.brain.add_input(c)
        for path in subpaths:
            line = list(map(ord, ",".join(map(str, path)) + "\n"))
            for c in line:
                self.brain.add_input(c)
        line = list(map(ord, "n\n"))
        for c in line:
            self.brain.add_input(c)
        self.brain.run()
        outputs = self.brain.get_all_outputs().split()

        return outputs[-1]
