# AOC19 day 17
from vacuumRobot import VacuumRobot


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def picture_to_scaffolding(picture):
    lines = picture.strip("\n").split("\n")
    x, y = 0, 0
    scaffolding = {}
    for row in range(len(lines)):
        for col in range(len(lines[0])):
            tile = lines[row][col]
            if tile == "#":
                scaffolding[(col, row)] = 1
            elif tile == ".":
                continue
            else:  # the robot
                scaffolding[(col, row)] = 1
                x, y = col, row
    return scaffolding, x, y


def alignment_sum(scaffolding):
    alignment = 0
    for x, y in scaffolding.keys():
        if (x-1, y) in scaffolding and \
           (x+1, y) in scaffolding and \
           (x, y-1) in scaffolding and \
           (x, y+1) in scaffolding:
            alignment += x * y
    return alignment


def run():
    data = load_data("Day17.txt")
    rob = VacuumRobot()
    rob.load(data)
    picture = rob.grab_camera()
    scaffolding, start_x, start_y = picture_to_scaffolding(picture)
    print(f"The sum of alignment parameters is {alignment_sum(scaffolding)}")
