# AOC19 day 21
from springDroid import SpringDroid


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day21.txt")
    droid = SpringDroid(data)
    code = ["OR D J", "OR A T", "AND B T", "AND C T", "NOT T T", "AND T J"]
    output = droid.run(code)
    for c in output:
        if c < 256:
            print(chr(c), end="")
        else:
            print(c)
