# AOC19 day 18
from doorMaze import DoorMaze


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day18.txt")
    maze = DoorMaze(data)
    shortest = maze.collect_all_keys()
    print(f"The shortest path to collect all the keys is {shortest} steps long")
