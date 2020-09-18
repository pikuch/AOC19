# AOC19 day 11
from collections import defaultdict
from emergencyHullPaintingRobot import EmHuPaR


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day11.txt")
    emhupar = EmHuPaR()
    emhupar.load(data)
    panels = defaultdict(lambda: 0)
    emhupar.run(panels)
    print(f"The robot paints {len(panels)} panels at least once")

    # for pos, col in panels.items():
    #    if col == 1
    #        print(f"{pos[0], pos[1]}")
