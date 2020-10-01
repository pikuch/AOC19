# AOC19 day 22


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_operations(data):
    ops = []
    for line in data.split("\n"):
        if line == "deal into new stack":
            ops.append((-1, 0))
        elif line[:19] == "deal with increment":
            ops.append([2, int(line.split()[3])])
        elif line[:3] == "cut":
            ops.append([1, int(line.split()[1])])
        else:
            print(f"Unrecognized operation: {line}")
            exit(1)
    return ops


def run():
    data = load_data("Day22test.txt")
    ops = parse_operations(data)
    deck = list(range(10))

