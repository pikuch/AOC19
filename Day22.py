# AOC19 day 22


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_operations(data):
    ops = []
    for line in data.split("\n"):
        if line == "deal into new stack":
            ops.append(("REV", 0))
        elif line[:19] == "deal with increment":
            ops.append(["MOD", int(line.split()[3])])
        elif line[:3] == "cut":
            ops.append(["CUT", int(line.split()[1])])
        else:
            print(f"Unrecognized operation: {line}")
            exit(1)
    return ops


def shuffle(deck, ops):
    for op in ops:
        if op[0] == "REV":
            deck = deck[::-1]
        elif op[0] == "CUT":
            deck = deck[op[1]:] + deck[:op[1]]
        else:  # deal with increment
            new_deck = deck.copy()
            for i in range(len(deck)):
                new_deck[(i*op[1]) % len(deck)] = deck[i]
            deck = new_deck
    return deck


# def track_back(pos, count, ops):
#     for op in reversed(ops):
#         if op[0] == -1:
#             pos = count - 1 - pos
#         elif op[0] == 1:
#             pos = (pos + op[1]) % count
#         else:  # deal with increment
#             n = 0
#             while (n * count + pos) % op[1] != 0:
#                 n += 1
#             pos = (n * count + pos) // op[1]
#     return pos


def parse_transformation(data, count):
    multiplier = 1
    offset = 0
    for line in data.split("\n"):
        if line == "deal into new stack":
            multiplier *= -1
            offset += multiplier
        elif line[:19] == "deal with increment":
            multiplier *= pow(int(line.split()[3]), count - 2, count)
        elif line[:3] == "cut":
            offset += int(line.split()[1]) * multiplier
        multiplier %= count
        offset %= count
    return multiplier, offset


def get_card_after_shuffles(pos, shuffles, multiplier, offset, count):
    increment = pow(multiplier, shuffles, count)
    final_offset = (offset * (1 - increment) * pow((1 - multiplier) % count, count - 2, count)) % count
    return (final_offset + pos * increment) % count


def run():
    data = load_data("Day22.txt")
    ops = parse_operations(data)
    deck = list(range(10007))
    deck = shuffle(deck, ops)
    print(f"After shuffling, card 2019 is at position {deck.index(2019)}")

    count = 119315717514047
    multiplier, offset = parse_transformation(data, count)
    pos = 2020
    shuffles = 101741582076661
    card = get_card_after_shuffles(pos, shuffles, multiplier, offset, count)
    print(f"Card at position {pos} after {shuffles} shuffles is {card}")
