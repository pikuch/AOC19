# AOC19 day 20
import numpy as np
from collections import deque


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_input(data):
    lines = data.split("\n")
    # make sure the lines are long enough
    max_line = 0
    for line in lines:
        if len(line) > max_line:
            max_line = len(line)
    max_line += 2
    for i in range(len(lines)):
        lines[i] = lines[i] + " " * (max_line - len(lines[i]))

    portals = {}
    maze = np.ones((len(lines), len(lines[0])), dtype=np.uint8)
    for row in range(maze.shape[0]):
        for col in range(maze.shape[1]):
            if row == 0 or row == maze.shape[0] - 1 or col == 0 or col == maze.shape[1] - 1:
                continue
            if lines[row][col] == "#" or lines[row][col] == " ":
                maze[row, col] = 1
            elif lines[row][col] == ".":
                maze[row, col] = 0
            else:  # a portal
                if lines[row-1][col] == ".":  # bottom wall
                    portal_name = lines[row][col] + lines[row+1][col]
                    maze[row+1, col] = 1
                    if portal_name in portals:
                        portals[portal_name].append(((row-1, col), (row, col)))
                    else:
                        portals[portal_name] = [((row-1, col), (row, col))]
                elif lines[row+1][col] == ".":  # top wall
                    portal_name = lines[row-1][col] + lines[row][col]
                    maze[row-1, col] = 1
                    if portal_name in portals:
                        portals[portal_name].append(((row+1, col), (row, col)))
                    else:
                        portals[portal_name] = [((row+1, col), (row, col))]
                elif lines[row][col-1] == ".":  # right wall
                    portal_name = lines[row][col] + lines[row][col+1]
                    maze[row, col+1] = 1
                    if portal_name in portals:
                        portals[portal_name].append(((row, col-1), (row, col)))
                    else:
                        portals[portal_name] = [((row, col-1), (row, col))]
                elif lines[row][col+1] == ".":  # left wall
                    portal_name = lines[row][col-1] + lines[row][col]
                    maze[row, col-1] = 1
                    if portal_name in portals:
                        portals[portal_name].append(((row, col+1), (row, col)))
                    else:
                        portals[portal_name] = [((row, col+1), (row, col))]
                else:  # not a portal, just a letter in the middle
                    continue
                maze[row, col] = 2
    links = {}
    for name, pos in portals.items():
        if name != "AA" and name != "ZZ":
            links[(pos[0][1])] = pos[1][0]
            links[(pos[1][1])] = pos[0][0]
    # start and stop are special cases
    maze[portals["AA"][0][1]] = 1
    maze[portals["ZZ"][0][1]] = 3
    return maze, links, portals["AA"][0][0], portals["ZZ"][0][0]


def find_shortest_path(maze, links, start, stop):
    visited = set()
    visited.add(start)
    to_check = deque()
    to_check.append((start[0], start[1], 0))
    while len(to_check):
        row, col, dist = to_check.popleft()
        if (row, col) == stop:
            return dist
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            new_row, new_col = row+dr, col+dc
            if maze[new_row, new_col] == 1:
                continue
            else:
                if (new_row, new_col) not in visited:
                    if maze[new_row, new_col] == 2:
                        new_row, new_col = links[(new_row, new_col)]
                    visited.add((new_row, new_col))
                    to_check.append((new_row, new_col, dist + 1))

    return -1  # not found


def run():
    data = load_data("Day20.txt")
    maze, links, start, stop = parse_input(data)
    shortest = find_shortest_path(maze, links, start, stop)
    print(f"The shortest path from AA to ZZ is {shortest}")
