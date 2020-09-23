# AOC19 day 18
import numpy as np
from itertools import permutations
from collections import deque


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_maze(data):
    lines = data.split("\n")
    maze = np.zeros((len(lines), len(lines[0])), dtype=np.uint8)
    keys = {}
    doors = {}
    row0, col0 = 0, 0
    for row in range(len(lines)):
        for col in range(len(lines[0])):
            tile = lines[row][col]
            if tile == "#":
                maze[row, col] = 1
            elif tile == ".":
                maze[row, col] = 0
            elif tile == "@":
                maze[row, col] = 0
                row0, col0 = row, col
            else:
                if tile.isupper():
                    maze[row, col] = 1
                    doors[tile] = (row, col)
                else:
                    maze[row, col] = 2
                    keys[tile] = (row, col)
                    keys[(row, col)] = tile

    return maze, keys, doors, row0, col0


def find_distance(maze, keys, doors, row, col, target):
    visited = set()
    visited.add((row, col))
    to_check = deque()
    to_check.append((row, col, 0))
    while len(to_check):
        r, c, dist = to_check.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            rr, cc = r + dr, c + dc
            if keys[target] == (rr, cc):
                return dist + 1
            if (rr, cc) not in visited and maze[rr, cc] == 0:
                visited.add((rr, cc))
                to_check.append((rr, cc, dist + 1))
    return None


# try to collect the keys in given order, return steps taken or None if there is no path
def collect_keys(maze, keys, doors, row, col, key_order):
    total_dist = 0
    for target in key_order:
        dist = find_distance(maze, keys, doors, row, col, target)
        if dist is not None:
            total_dist += dist
            row, col = keys[target]
            maze = maze.copy()
            maze[keys[target]] = 0
            if target.upper() in doors:
                maze[doors[target.upper()]] = 0
        else:
            return None
    return total_dist


# check all possible key collecting paths and find the shortest one
def shortest_all_keys_path(maze, keys, doors, row, col):
    shortest = 9**9
    for key_order in permutations(keys.keys()):
        steps = collect_keys(maze, keys, doors, row, col, key_order)
        if steps is not None:
            if steps < shortest:
                shortest = steps
    return shortest


# check which keys are possible
def possible_keys(maze, keys, doors, row, col):
    options = []
    visited = set()
    visited.add((row, col))
    to_check = deque()
    to_check.append((row, col, 0))
    while len(to_check):
        r, c, dist = to_check.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            rr, cc = r + dr, c + dc
            if maze[rr, cc] == 1:
                continue
            elif maze[rr, cc] == 2:
                options.append((keys[(rr, cc)], dist + 1))
            elif (rr, cc) not in visited and maze[rr, cc] == 0:
                visited.add((rr, cc))
                to_check.append((rr, cc, dist + 1))
    return options


# find the shortest path to all the keys by considering possibilities first
def shortest_path_fast(maze, keys, doors, row, col):
    options = possible_keys(maze, keys, doors, row, col)
    min_dist = None
    for grab, new_dist in options:
        new_maze = maze.copy()
        new_maze[keys[grab]] = 0
        if grab.upper() in doors:
            new_maze[doors[grab.upper()]] = 0
        new_keys = keys.copy()
        del new_keys[keys[grab]]
        del new_keys[grab]
        if len(new_keys):
            result = shortest_path_fast(new_maze, new_keys, doors, keys[grab][0], keys[grab][1])
            if result is None:
                continue
            dist = new_dist + result
            if min_dist is None:
                min_dist = dist
            elif dist < min_dist:
                min_dist = dist
        else:
            return new_dist
    return min_dist


def run():
    data = load_data("Day18test5.txt")
    maze, keys, doors, row, col = parse_maze(data)
    print(f"The shortest path to collect all the keys is {shortest_path_fast(maze, keys, doors, row, col)} steps long")
