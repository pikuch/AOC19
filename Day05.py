# AOC19 day 05
from intcode_v1 import Intcode


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day05.txt")

    comp = Intcode()
    comp.load(data)
    comp.inputs.append(1)
    comp.run()
    print(f"The outputs of the diagnostic program are: {' '.join(list(map(str, comp.outputs)))}")

    comp.load(data)
    comp.inputs.append(5)
    comp.run()
    print(f"The output of the thermal radiator controller is: {' '.join(list(map(str, comp.outputs)))}")
