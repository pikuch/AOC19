# AOC19 day 09
from intcode import Intcode


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day09.txt")
    comp = Intcode()
    comp.load(data)
    comp.add_input(1)
    comp.run()
    print(f"The BOOST keycode is {list(comp.outputs)[0]}")
