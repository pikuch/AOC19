# AOC19 day 11
from collections import defaultdict
from emergencyHullPaintingRobot import EmHuPaR


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def show(panels):
    min_x, max_x = 0, 0
    min_y, max_y = 0, 0
    for x, y in panels.keys():
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x, y) in panels:
                if panels[(x, y)] == 1:
                    print("#", end="")
                else:
                    print(" ", end="")
            else:
                print(" ", end="")
        print()


def run():
    data = load_data("Day11.txt")
    emhupar = EmHuPaR()
    emhupar.load(data)
    panels = defaultdict(lambda: 0)
    emhupar.run(panels)
    print(f"The robot paints {len(panels)} panels at least once")

    emhupar = EmHuPaR()
    emhupar.load(data)
    panels = defaultdict(lambda: 0)
    panels[(0, 0)] = 1
    emhupar.run(panels)

    show(panels)
