# AOC19 day 21
from springDroid import SpringDroid
from itertools import product


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def is_survivable(floor, pos):
    if pos >= len(floor):
        return True
    if not floor[pos]:
        return False
    return is_survivable(floor, pos+1) or is_survivable(floor, pos+4)


def generate_codes(n):
    items2 = ["T", "J"]
    items1 = ["T", "J"] + list(map(lambda a: chr(ord("A") + a), list(range(n))))
    ops = ("AND", "OR", "NOT")
    all_instructions = list(product(ops, items1, items2))
    for length in range(1, 16):
        for code in product(all_instructions, repeat=length):
            yield code


def execute_code(code, state):
    # set up registers
    regs = {"T": 0, "J": 0}
    for i in range(len(state)):
        regs[chr(ord("A") + i)] = state[i]
    # execute code
    for inst in code:
        if inst[0] == "AND":
            regs[inst[2]] = regs[inst[1]] & regs[inst[2]]
        elif inst[0] == "OR":
            regs[inst[2]] = regs[inst[1]] | regs[inst[2]]
        elif inst[0] == "NOT":
            regs[inst[2]] = not regs[inst[1]]
        else:
            print("Illegal instruction")
            exit(1)
    return regs["J"]


def verify_code(code, actions):
    for state, response in actions.items():
        if execute_code(code, state) != response:
            return False
    return True


def find_codes(n):
    floors = list(product(range(2), repeat=n))
    actions = {}
    for floor in floors:
        stay = is_survivable(floor, 0)
        jump = is_survivable(floor, 3)
        if stay != jump:  # it makes a difference
            actions[floor] = jump
    # from experience
    actions[(1,1,1,1,0,1,0,1,0)] = False

    # for bits, outcome in actions.items():
    #     print(" ".join(map(str, bits)), end="")
    #     if outcome:
    #         print(" = 1")
    #     else:
    #         print(" = 0")
    # exit(1)

    code_generator = generate_codes(n)
    code = []
    while True:
        code = next(code_generator)
        if verify_code(code, actions):
            break
    return list(map(lambda a: " ".join(a), code))


def run():
    data = load_data("Day21.txt")
    droid = SpringDroid(data)
    code4 = ["OR D J", "OR A T", "AND B T", "AND C T", "NOT T T", "AND T J"]
    output = droid.walk(code4)
    for c in output:
        if c < 256:
            print(chr(c), end="")
        else:
            print(c)
    droid = SpringDroid(data)
    code9 = find_codes(9)
    print(f"Trying {code9}")
    output = droid.run(code9)
    for c in output:
        if c < 256:
            print(chr(c), end="")
        else:
            print(c)
