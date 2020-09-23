from intcode import Intcode


class VacuumRobot:
    def __init__(self):
        self.brain = Intcode()

    def load(self, code):
        self.brain.load(code)

    def grab_camera(self):
        self.brain.run()
        return "".join(map(chr, map(int, self.brain.get_all_outputs().split())))
