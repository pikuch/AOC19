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


def shuffle(deck, ops):
    for op in ops:
        if op[0] == -1:
            deck = deck[::-1]
        elif op[0] == 1:
            deck = deck[op[1]:] + deck[:op[1]]
        else:  # deal with increment
            new_deck = deck.copy()
            for i in range(len(deck)):
                new_deck[(i*op[1]) % len(deck)] = deck[i]
            deck = new_deck
    return deck


def run():
    data = load_data("Day22test4.txt")
    ops = parse_operations(data)
    deck = list(range(10))
    deck = shuffle(deck, ops)
    print(f"Shuffled deck: {' '.join(map(str, deck))}")
