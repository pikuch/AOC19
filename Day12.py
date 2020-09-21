# AOC19 day 12
import numpy as np


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


def run():
    data = load_data("Day12.txt")
    state = parse_data(data)
    print(state)
    for i in range(1000):
        update(state)
    print(f"The total energy of the system after 1000 steps is {calculate_total_energy(state)}")