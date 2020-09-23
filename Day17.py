# AOC19 day 17
from vacuumRobot import VacuumRobot


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def picture_to_scaffolding(picture):
    lines = picture.strip("\n").split("\n")
    x, y = 0, 0
    scaffolding = {}
    for row in range(len(lines)):
        for col in range(len(lines[0])):
            tile = lines[row][col]
            if tile == "#":
                scaffolding[(col, row)] = 1
            elif tile == ".":
                continue
            else:  # the robot
                scaffolding[(col, row)] = 1
                x, y = col, row
                dirs = {"^": 0, ">": 1, "v": 2, "<": 3}
                direction = dirs[tile]

    return scaffolding, x, y, direction


def alignment_sum(scaffolding):
    alignment = 0
    for x, y in scaffolding.keys():
        if (x - 1, y) in scaffolding and \
                (x + 1, y) in scaffolding and \
                (x, y - 1) in scaffolding and \
                (x, y + 1) in scaffolding:
            alignment += x * y
    return alignment


def ahead(x, y, d):
    dx = {0: 0, 1: 1, 2: 0, 3: -1}
    dy = {0: -1, 1: 0, 2: 1, 3: 0}
    return x + dx[d], y + dy[d]


def left(x, y, d):
    dx = {0: 0, 1: 1, 2: 0, 3: -1}
    dy = {0: -1, 1: 0, 2: 1, 3: 0}
    return x + dx[(d + 3) % 4], y + dy[(d + 3) % 4]


def right(x, y, d):
    dx = {0: 0, 1: 1, 2: 0, 3: -1}
    dy = {0: -1, 1: 0, 2: 1, 3: 0}
    return x + dx[(d + 1) % 4], y + dy[(d + 1) % 4]


def make_path(scaffolding, x, y, direction):
    path = []
    while True:
        steps = 0
        while ahead(x, y, direction) in scaffolding:
            steps += 1
            x, y = ahead(x, y, direction)
        if steps > 0:
            path.append(steps)
        if left(x, y, direction) in scaffolding:
            direction = (direction + 3) % 4
            path.append("L")
        elif right(x, y, direction) in scaffolding:
            direction = (direction + 1) % 4
            path.append("R")
        else:  # the end of the path
            break
    return path


def get_reminder(path, a, b):
    without_ab = []
    i = 0
    while i < len(path):
        if path[i:i+len(a)] == a:
            if i > 0:
                without_ab.extend(path[:i])
            path = path[i+len(a):]
            i = 0
        elif path[i:i + len(b)] == b:
            if i > 0:
                without_ab.extend(path[:i])
            path = path[i + len(b):]
            i = 0
        else:
            i += 1
    without_ab.extend(path)

    # try to divide without_ab
    for length in range(1, 11):
        subpath = without_ab[:length]
        if without_ab == subpath * (len(without_ab) // len(subpath)):
            return subpath

    return None


def get_order(path, a, b, c):
    order = []
    index = 0
    while index < len(path) - 1:
        if path[index:index + len(a)] == a:
            order.append("A")
            index += len(a)
        elif path[index:index + len(b)] == b:
            order.append("B")
            index += len(b)
        elif path[index:index + len(c)] == c:
            order.append("C")
            index += len(c)
        else:
            print(f"Failed to split the path at index {index}, done: {order}")
            return order
    return order


def split_path(path):
    for length1 in range(1, 11):
        for length2 in range(1, 11):
            reminder = get_reminder(path[length1 + length2:], path[:length1], path[length1:length1+length2])
            if reminder is not None and len(reminder) <= 10:
                return get_order(path, path[:length1], path[length1:length1+length2], reminder), \
                       [path[:length1], path[length1:length1+length2], reminder]


def run():
    data = load_data("Day17.txt")
    rob = VacuumRobot()
    rob.load(data)
    picture = rob.grab_camera()
    scaffolding, start_x, start_y, direction = picture_to_scaffolding(picture)
    print(f"The sum of alignment parameters is {alignment_sum(scaffolding)}")

    path = make_path(scaffolding, start_x, start_y, direction)
    order, subpaths = split_path(path)
    rob.load(data)
    dust = rob.run_path(order, subpaths)

    print(f"The robot collected {dust} dust")
