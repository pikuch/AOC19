# AOC19 day 12
import numpy as np
from math import gcd


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_data(data):
    state = np.zeros((2, 4, 3), dtype=np.int32)
    lines = data.split("\n")
    for i in range(len(lines)):
        words = lines[i].translate(str.maketrans("<>,=xyz", "       ")).split()
        state[0, i] = list(map(int, words))
    return state


def update(state):
    for i in range(4):
        state[1, i] += np.sum(np.sign(state[0, :] - state[0, i]), axis=0)
    state[0] += state[1]


def calculate_total_energy(state):
    return np.sum(np.sum(np.abs(state[0, :]), axis=1) * np.sum(np.abs(state[1, :]), axis=1), axis=0)


def find_repetitions(state, axis):
    reps = 0
    seen = set(str(state[:, :, axis]))
    n = 0
    while not reps:
        update(state)
        if str(state[:, :, axis]) in seen:
            reps = n
            print(f"found axis {axis+1} at {n} repetitions")
            return reps
        else:
            seen.add(str(state[:, :, axis]))
        n += 1


def lcm(a, b):
    return a * b // gcd(a, b)


def run():
    data = load_data("Day12.txt")
    state = parse_data(data)
    for i in range(1000):
        update(state)
    print(f"The total energy of the system after 1000 steps is {calculate_total_energy(state)}")

    reps = []
    print("Looking for repetitions...")
    for axis in range(3):
        state = parse_data(data)
        reps.append(find_repetitions(state, axis))
    print(f"The planets repeat themselves along axis after {reps} steps")
    system_repetition = lcm(lcm(reps[0], reps[1]), reps[2])
    print(f"so the whole system repeats itself after {system_repetition} steps")
