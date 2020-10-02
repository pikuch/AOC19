# AOC19 day 24
import numpy as np


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_data(data):
    lines = data.split("\n")
    if len(lines) != 5 or len(lines[0]) != 5:
        print(f"Input has wrong dimensions! ({len(lines)}x{len(lines[0])})")
        exit(1)
    eris = np.zeros((7, 7), dtype=np.uint8)
    for row in range(5):
        for col in range(5):
            if lines[row][col] == "#":
                eris[row+1, col+1] = 1
    return eris


def show_state(eris):
    for row in range(5):
        for col in range(5):
            if eris[row+1, col+1]:
                print("██", end="")
            else:
                print("░░", end="")
        print()


def infest(eris):
    neighbours = np.zeros((5, 5), dtype=np.uint8)
    for row in range(5):
        for col in range(5):
            neighbours[row, col] = eris[row, col+1] + eris[row+2, col+1] + eris[row+1, col] + eris[row+1, col+2]
    for row in range(5):
        for col in range(5):
            if eris[row+1, col+1]:
                if neighbours[row, col] != 1:
                    eris[row + 1, col + 1] = 0
            else:
                if neighbours[row, col] == 1 or neighbours[row, col] == 2:
                    eris[row + 1, col + 1] = 1


def calculate_biodiversity(eris):
    return sum(eris[1:6, 1:6].flat * np.power(2, np.arange(25)))


def run():
    data = load_data("Day24.txt")
    eris = parse_data(data)
    seen = set()
    while True:
        infest(eris)
        show_state(eris)
        print()
        if str(eris) in seen:
            break
        else:
            seen.add(str(eris))
    print(f"The biodiversity rating of the first tile that appears twice is {calculate_biodiversity(eris)}")
