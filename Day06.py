# AOC19 day 06
from collections import defaultdict


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_orbits(data):
    orbits = defaultdict(lambda: [])
    for line in data.split("\n"):
        planets = line.split(")")
        orbits[planets[0]].append(planets[1])
    return orbits


def count_total_orbits(current, level, orbits):
    return level + sum(map(lambda a: count_total_orbits(a, level+1, orbits), orbits[current]))


def run():
    data = load_data("Day06.txt")
    orbits = parse_orbits(data)
    total_orbits = count_total_orbits("COM", 0, orbits)
    print(f"The total number of direct and indirect orbits is {total_orbits}")
