# AOC19 day 02
from intcode import Intcode


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day02.txt")
    comp = Intcode()
    comp.load(data)
    comp.code[1], comp.code[2] = 12, 2
    comp.run()
    print(comp.code[0])
