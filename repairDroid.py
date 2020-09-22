from intcode import Intcode


class RepairDroid:
    def __init__(self):
        self.brain = Intcode()
        self.x = 0
        self.y = 0

    def load(self, code):
        self.brain.load(code)

    def show_map(self, corridors):
        x0, x1, y0, y1 = 0, 0, 0, 0
        for place in corridors.keys():
            if place[0] < x0:
                x0 = place[0]
            if place[0] > x1:
                x1 = place[0]
            if place[1] < y0:
                y0 = place[1]
            if place[1] > y1:
                y1 = place[1]
        for y in range(y0, y1+1):
            for x in range(x0, x1+1):
                if x == self.x and y == self.y:
                    c = "[]"
                elif (x, y) in corridors:
                    if corridors[(x, y)] == -1:
                        c = "░░"
                    elif corridors[(x, y)] == -2:
                        c = "██"
                    elif corridors[(x, y)] == -10:
                        c = "GG"
                else:
                    c = "  "
                print(c, end="")
            print()

    def explore(self, corridors):
        direction = 0
        dir_to_movement = {0: 1, 1: 4, 2: 2, 3: 3}
        dx = {0: 0, 1: 1, 2: 0, 3: -1}
        dy = {0: -1, 1: 0, 2: 1, 3: 0}
        while True:
            if self.x == 0 and self.y == 0 and len(corridors) > 10:  # back at the beginning
                break
            self.brain.add_input(dir_to_movement[direction])
            self.brain.run()
            info = self.brain.get_output()
            if info == 0:  # hit a wall
                corridors[(self.x + dx[direction], self.y + dy[direction])] = -2
                direction = (direction + 1) % 4
            elif info == 1:  # moved
                self.x += dx[direction]
                self.y += dy[direction]
                corridors[(self.x, self.y)] = -1
                direction = (direction + 3) % 4
            elif info == 2:  # found generator
                self.x += dx[direction]
                self.y += dy[direction]
                corridors[(self.x, self.y)] = -10
                direction = (direction + 3) % 4
        self.show_map(corridors)
