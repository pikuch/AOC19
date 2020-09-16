# AOC19 day 03

def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_data(data):
    wires = []
    for line in data.split("\n"):
        wire = []
        for word in line.split(","):
            wire.append((word[0], int(word[1:])))
        wires.append(wire)
    return wires


def list_places(wires):
    places_list = []
    dx = {"U": 0, "D": 0, "L": -1, "R": 1}
    dy = {"U": -1, "D": 1, "L": 0, "R": 0}
    for wire in wires:
        places = {}
        steps = 0
        x, y = 0, 0
        for direction, movement in wire:
            for _ in range(movement):
                x += dx[direction]
                y += dy[direction]
                steps += 1
                if (x, y) not in places:
                    places[(x, y)] = steps
        places_list.append(places)
    return places_list


# finds all the crossings between wires
def find_crossings(wires):
    places = list_places(wires)
    crossings = {}
    for position1, time1 in places[0].items():
        for position2, time2 in places[1].items():
            if position1 == position2 and position1 not in crossings:
                crossings[position1] = time1 + time2
    return crossings


def run():
    data = load_data("Day03test.txt")
    wires = parse_data(data)
    crossings = find_crossings(wires)
    closest = sorted(list(crossings.keys()), key=lambda a: abs(a[0]) + abs(a[1]))[0]
    print(f"The closest crossing is {abs(closest[0]) + abs(closest[1])} steps away")
