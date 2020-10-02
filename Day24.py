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


def parse_recursive(data):
    lines = data.split("\n")
    reris = {}
    reris[0] = np.zeros((5, 5), dtype=np.uint8)
    reris[-1] = np.zeros((5, 5), dtype=np.uint8)
    reris[1] = np.zeros((5, 5), dtype=np.uint8)
    for row in range(5):
        for col in range(5):
            if lines[row][col] == "#":
                reris[0][row, col] = 1
    return reris


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


def count_neighbours(level, row, col, reris):
    neighbours = 0
    # up
    if row == 3 and col == 2:
        if level + 1 in reris:
            neighbours += np.sum(reris[level + 1][4, :])
    elif row == 0:
        if level - 1 in reris:
            neighbours += reris[level - 1][1, 2]
    else:
        neighbours += reris[level][row - 1, col]
    # down
    if row == 1 and col == 2:
        if level + 1 in reris:
            neighbours += np.sum(reris[level + 1][0, :])
    elif row == 4:
        if level - 1 in reris:
            neighbours += reris[level - 1][3, 2]
    else:
        neighbours += reris[level][row + 1, col]
    # left
    if row == 2 and col == 3:
        if level + 1 in reris:
            neighbours += np.sum(reris[level + 1][:, 4])
    elif col == 0:
        if level - 1 in reris:
            neighbours += reris[level - 1][2, 1]
    else:
        neighbours += reris[level][row, col-1]
    # right
    if row == 2 and col == 1:
        if level + 1 in reris:
            neighbours += np.sum(reris[level + 1][:, 0])
    elif col == 4:
        if level - 1 in reris:
            neighbours += reris[level - 1][2, 3]
    else:
        neighbours += reris[level][row, col+1]

    return neighbours


def infest_recursive(reris):
    lowest_level, highest_level = 0, 0
    neighbours = {}

    # set up neighbours and check limits
    for level in reris.keys():
        if level < lowest_level:
            lowest_level = level
        if level > highest_level:
            highest_level = level
        neighbours[level] = np.zeros((5, 5), dtype=np.uint8)

    # count neighbours
    for level in reris.keys():
        for row in range(5):
            for col in range(5):
                if not (row == 2 and col == 2):
                    neighbours[level][row, col] = count_neighbours(level, row, col, reris)

    # apply infestation
    for level in reris.keys():
        for row in range(5):
            for col in range(5):
                if not (row == 2 and col == 2):
                    if reris[level][row, col]:
                        if neighbours[level][row, col] != 1:
                            reris[level][row, col] = 0
                    else:
                        if neighbours[level][row, col] == 1 or neighbours[level][row, col] == 2:
                            reris[level][row, col] = 1

    # add levels if needed
    if np.sum(reris[lowest_level]):
        reris[lowest_level - 1] = np.zeros((5, 5), dtype=np.uint8)
    if np.sum(reris[highest_level]):
        reris[highest_level + 1] = np.zeros((5, 5), dtype=np.uint8)


def calculate_biodiversity(eris):
    return sum(eris[1:6, 1:6].flat * np.power(2, np.arange(25)))


def count_bugs(reris):
    bugs = 0
    for level in reris.keys():
        bugs += np.sum(reris[level])
    return bugs


def run():
    data = load_data("Day24test.txt")
    eris = parse_data(data)
    seen = set()
    while True:
        infest(eris)
        # show_state(eris)
        # print()
        if str(eris) in seen:
            break
        else:
            seen.add(str(eris))
    print(f"The biodiversity rating of the first tile that appears twice is {calculate_biodiversity(eris)}")

    # part 2

    reris = parse_recursive(data)
    for t in range(10):
        infest_recursive(reris)
    print(f"After 10 minutes there are {count_bugs(reris)} bugs on {len(reris)-2} levels")
