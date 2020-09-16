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


# finds all the crossings between wires
def find_crossings(wires):
    dx = {"U": 0, "D": 0, "L": -1, "R": 1}
    dy = {"U": -1, "D": 1, "L": 0, "R": 0}
    places = {}
    crossings = {}
    steps = 0
    x, y = 0, 0
    for direction, movement in wires[0]:
        for _ in range(movement):
            x += dx[direction]
            y += dy[direction]
            steps += 1
            if (x, y) not in places:
                places[(x, y)] = steps
    steps = 0
    x, y = 0, 0
    for direction, movement in wires[1]:
        for _ in range(movement):
            x += dx[direction]
            y += dy[direction]
            steps += 1
            if (x, y) in places and (x, y) not in crossings:
                crossings[(x, y)] = (places[(x, y)], steps)
    return crossings


def run():
    data = load_data("Day03.txt")
    wires = parse_data(data)
    crossings = find_crossings(wires)
    closest = sorted(list(crossings.keys()), key=lambda a: abs(a[0]) + abs(a[1]))[0]
    print(f"The closest crossing is {abs(closest[0]) + abs(closest[1])} steps away")
    shortest_time = sorted(list(crossings.values()), key=lambda a: a[0] + a[1])[0]
    print(f"The crossing closest in time is {sum(shortest_time)} steps away")
