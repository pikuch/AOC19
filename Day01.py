# AOC19 day 01


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def fuel_requirement(mass):
    return (mass // 3) - 2


def get_fuel_sum(masses):
    fuel = 0
    for mass in masses:
        fuel += fuel_requirement(mass)
    return fuel


def run():
    data = load_data("Day01.txt")
    masses = list(map(int, data.split("\n")))
    print(f"The sum of the fuel requirements is {get_fuel_sum(masses)}")
