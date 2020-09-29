# AOC19 day 21
from springDroid import SpringDroid


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day21.txt")
    droid = SpringDroid(data)
    output = droid.run("NOT A J")
    for c in output:
        print(c, end="")
