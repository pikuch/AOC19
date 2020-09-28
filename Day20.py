# AOC19 day 20
import numpy as np


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
    maze = np.zeros((len(lines), len(lines[0])), dtype=np.uint8)
    for row in range(maze.shape[0]):
        for col in range(maze.shape[1]):
            if row == 0 or row == maze.shape[0] - 1 or col == 0 or col == maze.shape[1] - 1:
                continue
            if lines[row][col] == "#":
                maze[row, col] = 1
            elif lines[row][col] == " " or lines[row][col] == ".":
                pass
            else:  # a portal
                portal_name = ""
                if lines[row-1][col] == ".":  # bottom wall
                    portal_name = lines[row][col] + lines[row+1][col]
                elif lines[row+1][col] == ".":  # top wall
                    portal_name = lines[row-1][col] + lines[row][col]
                elif lines[row][col-1] == ".":  # right wall
                    portal_name = lines[row][col] + lines[row][col+1]
                elif lines[row][col+1] == ".":  # left wall
                    portal_name = lines[row][col-1] + lines[row][col]
                else:  # not a portal, just a letter in the middle
                    continue
                maze[row, col] = 2
                if portal_name in portals:
                    portals[portal_name].append((row, col))
                else:
                    portals[portal_name] = [(row, col)]
    return maze, portals


def run():
    data = load_data("Day20test.txt")
    maze, portals = parse_input(data)
    #shortest = find_shortest_path(maze, portals)
    #print(f"The shortest path from AA to ZZ is {shortest}")
