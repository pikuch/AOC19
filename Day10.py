# AOC19 day 10
from math import gcd


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


def run():
    data = load_data("Day10test.txt").split("\n")
    asteroids, max_x, max_y = parse_asteroids(data)
    x, y, detected = find_best_location(asteroids, max_x, max_y)
    print(f"The best place is at {x}, {y} and it detects {detected} asteroids")
