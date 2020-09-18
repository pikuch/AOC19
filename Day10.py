# AOC19 day 10
from math import gcd, atan2, pi


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_asteroids(data):
    asteroids = []
    for row in range(len(data)):
        for col in range(len(data[0])):
            if data[row][col] == "#":
                asteroids.append([col, row, 0])
    return asteroids, len(data[0]), len(data)


def detect(asteroids, place, max_x, max_y):
    visible = {}
    for aster in asteroids:
        if aster != place:
            visible[(aster[0] - place[0], aster[1] - place[1])] = True
    for aster in visible.keys():
        if not visible[aster]:
            continue
        if aster[0] == 0:
            step_x = 0
            step_y = aster[1] // abs(aster[1])
        elif aster[1] == 0:
            step_y = 0
            step_x = aster[0] // abs(aster[0])
        else:
            gcd_xy = gcd(abs(aster[0]), abs(aster[1]))
            step_x = aster[0] // gcd_xy
            step_y = aster[1] // gcd_xy
        multiplier = 0
        while abs(aster[0] + step_x * multiplier) < max_x and abs(aster[1] + step_y * multiplier) < max_y:
            multiplier += 1
            if (aster[0] + step_x * multiplier, aster[1] + step_y * multiplier) in visible:
                visible[(aster[0] + step_x * multiplier, aster[1] + step_y * multiplier)] = False
    detected = 0
    for aster in visible.values():
        if aster:
            detected += 1
    return detected


def find_best_location(asteroids, max_x, max_y):
    for aster in asteroids:
        aster[2] = detect(asteroids, aster, max_x, max_y)
    best = sorted(asteroids, key=lambda a: a[2])[-1]
    return tuple(best)


def find_200th_vaporized(asteroids, best_x, best_y):
    targets = []
    for aster in asteroids:
        if not (aster[0] == best_x and aster[1] == best_y):
            targets.append([aster[0] - best_x, aster[1] - best_y,
                            True, -atan2(aster[0] - best_x, aster[1] - best_y) + pi/2])
    targets.sort(key=lambda a: (a[3], abs(a[0]) + abs(a[1])))
    index = 0
    vaporized = 0
    last_angle = None
    while True:
        if targets[index][2] and targets[index][3] != last_angle:
            targets[index][2] = False
            last_angle = targets[index][3]
            vaporized += 1
            if vaporized == 200:
                return targets[index][0] + best_x, targets[index][1] + best_y

        index = (index + 1) % len(targets)


def run():
    data = load_data("Day10.txt").split("\n")
    asteroids, max_x, max_y = parse_asteroids(data)
    best_x, best_y, detected = find_best_location(asteroids, max_x, max_y)
    print(f"The best place is at {best_x}, {best_y} and it detects {detected} asteroids")

    x, y = find_200th_vaporized(asteroids, best_x, best_y)
    print(f"The 200th asteroid to be vaporized is at {x}, {y}, so the answer is {100*x+y}")
