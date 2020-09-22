# AOC19 day 14
from math import ceil


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_recipes(data):
    chem = {}
    for line in data.split("\n"):
        words = line.translate(str.maketrans(",=>", "   ")).split()
        for i in range(len(words)//2):
            if words[2*i+1] not in chem:
                chem[words[2*i+1]] = {"recipe": [], "output": 0}
        chem[words[-1]]["output"] = int(words[-2])
        for i in range(len(words)//2-1):
            chem[words[-1]]["recipe"].append([int(words[2*i]), words[2*i+1]])
    return chem


def decompose(chem, amount):
    need = {}
    for c in chem.keys():
        need[c] = 0
    need["FUEL"] = amount
    unfulfilled = True
    while unfulfilled:
        unfulfilled = False
        for k, v in need.items():
            if k != "ORE" and v > 0:
                unfulfilled = True
                times_needed = ceil(v/chem[k]["output"])
                for ingredient in chem[k]["recipe"]:
                    need[ingredient[1]] += ingredient[0] * times_needed
                need[k] -= times_needed * chem[k]["output"]
    return need["ORE"]


def calculate_fuel(chem, ore, ore_needed):
    guess = ore // ore_needed
    guess_jump = decompose(chem, guess)
    while guess_jump > 0:
        projected_ore = decompose(chem, guess + guess_jump)
        if projected_ore < ore:
            guess += guess_jump
        else:
            guess_jump //= 2
    return guess


def run():
    data = load_data("Day14.txt")
    chem = parse_recipes(data)
    ore_needed = decompose(chem, 1)
    print(f"We need {ore_needed} ore to produce 1 fuel")

    print(f"With 1 trillion ore we could make {calculate_fuel(chem, 10**12, ore_needed)} fuel")
