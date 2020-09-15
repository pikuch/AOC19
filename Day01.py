# AOC19 day 01


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def fuel_requirement(mass):
    return (mass // 3) - 2


def corrected_fuel_requirement(mass):
    fuel = 0
    while True:
        additional_fuel = (mass // 3) - 2
        if additional_fuel <= 0:
            return fuel
        fuel += additional_fuel
        mass = additional_fuel


def get_fuel_sum(masses):
    fuel = 0
    for mass in masses:
        fuel += fuel_requirement(mass)
    return fuel


def get_corrected_fuel_sum(masses):
    fuel = 0
    for mass in masses:
        fuel += corrected_fuel_requirement(mass)
    return fuel


def run():
    data = load_data("Day01.txt")
    masses = list(map(int, data.split("\n")))
    print(f"The sum of fuel requirements is {get_fuel_sum(masses)}")
    print(f"The real sum of fuel requirements is {get_corrected_fuel_sum(masses)}")
