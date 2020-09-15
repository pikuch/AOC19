# AOC19 day 02
from intcode import Intcode
from itertools import product


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day02.txt")
    comp = Intcode()
    comp.load(data)
    comp.set({1: 12, 2: 2})
    comp.run()
    print(f"The first output is {comp.code[0]}")
    for a, b in product(range(100), range(100)):
        comp.load(data)
        comp.set({1: a, 2: b})
        comp.run()
        if comp.code[0] == 19690720:
            print(f"The first input to produce 19690720 is {a * 100 + b}")
            break
