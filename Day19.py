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


def calculate_santa_coordinates(data):
    ux = 20
    uy = 0
    while not ask_about_position(data, ux, uy):
        uy += 1
    dx = 0
    dy = 20
    while not ask_about_position(data, dx, dy):
        dx += 1

    last_ship_size = 0
    while ux - dx + 1 < 100 or dy - uy + 1 < 100:
        if ux - dx > dy - uy:
            # move down point
            dy += 1
            while ask_about_position(data, dx, dy) == 0:
                dx += 1
        else:
            # move up point
            ux += 1
            while ask_about_position(data, ux, uy) == 0:
                uy += 1
        new_size = min(ux - dx + 1, dy - uy + 1)
        if new_size > last_ship_size:
            print(f"\rLooking along the beam, ship size {new_size}/100", end="")
            last_ship_size = new_size
    print(" ...found!")
    return dx, uy


def run():
    data = load_data("Day19.txt")
    affected = show_tractor_beam(data, 50, 50)
    print(f"There are {affected} points affected by the tractor beam in the 50x50 area")
    x, y = calculate_santa_coordinates(data)
    print(f"The value derived from santa's ship coordinates is {x * 10000 + y}")
