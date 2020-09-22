# AOC19 day 15
from repairDroid import RepairDroid


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day15.txt")
    droid = RepairDroid()
    droid.load(data)
    corridors = {(0, 0): -1}
    droid.explore(corridors)


