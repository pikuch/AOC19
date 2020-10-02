# AOC19 day 25
from rescueDrone import RescueDrone
from collections import deque
from itertools import combinations


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    collect_list = deque()
    collect_list.extend(["w", "w", "w", "w",
                         "t dark matter",
                         "e", "s", "w",
                         "t food ration",
                         "e",
                         "t fixed point",
                         "n", "e", "s",
                         "t astronaut ice cream",
                         "s",
                         "t polygon",
                         "e",
                         "t easter egg",
                         "e",
                         "t weather machine",
                         "n"])
    items = ["dark matter", "food ration", "fixed point", "astronaut ice cream", "polygon", "easter egg", "weather machine"]
    for count in range(1, 7):
        for dropped in combinations(items, count):
            for item in dropped:
                collect_list.append("d " + item)
            collect_list.append("n")
            for item in dropped:
                collect_list.append("t " + item)
    data = load_data("Day25.txt")
    rescue = RescueDrone(data)
    rescue.act()
    while True:
        if len(collect_list):
            command = collect_list.popleft()
        else:
            command = input(">")
        rescue.act(command)
