# AOC19 day 15
from collections import deque
from repairDroid import RepairDroid


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def find_distance(corridors):
    to_check = deque()
    to_check.append((0, 0, 0))
    corridors[(0, 0)] = 0
    while len(to_check):
        x, y, dist = to_check.popleft()
        for xx, yy in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if corridors[(xx, yy)] < 0:
                if corridors[(xx, yy)] == -1:
                    corridors[(xx, yy)] = dist + 1
                    to_check.append((xx, yy, dist + 1))
                elif corridors[(xx, yy)] == -10:
                    return dist + 1
    return -1  # no path


def fill_with_oxygen(corridors):
    x, y, time = 0, 0, 0
    for k, v in corridors.items():
        if v == -10:
            x = k[0]
            y = k[1]
            break
    to_fill = deque()
    to_fill.append((x, y, 0))
    corridors[(x, y)] = 1000  # oxygen
    while len(to_fill):
        x, y, time = to_fill.popleft()
        for xx, yy in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if corridors[(xx, yy)] != -2 and corridors[(xx, yy)] != 1000:
                corridors[(xx, yy)] = 1000
                to_fill.append((xx, yy, time + 1))
    return time


def run():
    data = load_data("Day15.txt")
    droid = RepairDroid()
    droid.load(data)
    corridors = {(0, 0): -1}
    droid.explore(corridors)
    print(f"The repair droid can get to the oxygen system in {find_distance(corridors)} steps")
    print(f"The area will be filled with oxygen after {fill_with_oxygen(corridors)} minutes")
