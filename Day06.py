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


def get_path_to(object, orbits):
    path = []
    while object != "COM":
        for body in orbits:
            if object in orbits[body]:
                path.append(body)
                object = body
                break
    return list(reversed(path))


def count_transfers(objects, orbits):
    paths = []
    for i in range(len(objects)):
        paths.append(get_path_to(objects[i], orbits))
    for i in range(min(len(paths[0]), len(paths[1]))):
        if paths[0][i] != paths[1][i]:
            break
    return len(paths[0]) + len(paths[1]) - 2 * i


def run():
    data = load_data("Day06test2.txt")
    orbits = parse_orbits(data)
    total_orbits = count_total_orbits("COM", 0, orbits)
    print(f"The total number of direct and indirect orbits is {total_orbits}")

    transfers = count_transfers(["YOU", "SAN"], orbits)
    print(f"The total number of transfers needed to get YOU to SANTA is {transfers}")
