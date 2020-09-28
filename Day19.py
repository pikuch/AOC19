# AOC19 day 19
from intcode import Intcode


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def ask_about_position(data, x, y):
    beam = Intcode()
    beam.load(data)
    beam.add_input(x)
    beam.add_input(y)
    beam.run()
    return beam.get_output()


def show_tractor_beam(data, max_x, max_y):
    affected = 0
    for y in range(max_y):
        for x in range(max_x):
            if ask_about_position(data, x, y) == 1:
                affected += 1
                print("#", end="")
            else:
                print(".", end="")
        print()
    return affected


def run():
    data = load_data("Day19.txt")
    affected = show_tractor_beam(data, 20, 20)
    print(f"There are {affected} points affected by the tractor beam in the 50x50 area")
