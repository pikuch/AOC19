import numpy as np
from collections import deque


class DoorMaze:
    def __init__(self, data):
        lines = data.split("\n")
        self.EMPTY, self.WALL, self.KEY, self.DOOR = 0, 1, 2, 3
        self.maze = np.zeros((len(lines), len(lines[0])), dtype=np.uint8)
        self.keys = {}
        self.doors = {}
        self.key_locations = {}
        self.door_locations = {}
        self.blockers = {}
        self.key_distances = {}
        self.start_row = 0
        self.start_col = 0
        for row in range(len(lines)):
            for col in range(len(lines[0])):
                tile = lines[row][col]
                if tile == "#":
                    self.maze[row, col] = self.WALL
                elif tile == ".":
                    self.maze[row, col] = self.EMPTY
                elif tile == "@":
                    self.maze[row, col] = self.EMPTY
                    self.start_row = row
                    self.start_col = col
                else:  # keys and doors
                    if tile.isupper():
                        self.maze[row, col] = self.DOOR
                        self.doors[tile] = (row, col)
                        self.door_locations[(row, col)] = tile
                    else:
                        self.maze[row, col] = self.KEY
                        self.keys[tile] = (row, col)
                        self.key_locations[(row, col)] = tile
        self.keys["0"] = (self.start_row, self.start_col)
        self.key_locations[(self.start_row, self.start_col)] = "0"

    def split(self):
        self.maze[self.start_row-1, self.start_col] = self.WALL
        self.maze[self.start_row, self.start_col-1] = self.WALL
        self.maze[self.start_row, self.start_col] = self.WALL
        self.maze[self.start_row, self.start_col+1] = self.WALL
        self.maze[self.start_row+1, self.start_col] = self.WALL
        del self.keys["0"]
        self.keys["1"] = (self.start_row-1, self.start_col-1)
        self.key_locations[(self.start_row-1, self.start_col-1)] = "1"
        self.keys["2"] = (self.start_row+1, self.start_col-1)
        self.key_locations[(self.start_row+1, self.start_col-1)] = "2"
        self.keys["3"] = (self.start_row-1, self.start_col+1)
        self.key_locations[(self.start_row-1, self.start_col+1)] = "3"
        self.keys["4"] = (self.start_row+1, self.start_col+1)
        self.key_locations[(self.start_row+1, self.start_col+1)] = "4"

        self.key_distances = {}
        self.blockers = {}

        keys = list(self.keys.keys())
        for start in keys:
            self.measure_key_distances_from(start)
        for start in keys:
            self.detect_blocking(start)

    # start at key start and write distances to all encountered keys
    def measure_key_distances_from(self, start):
        visited = set()
        visited.add(self.keys[start])
        to_check = deque()
        to_check.append((self.keys[start][0], self.keys[start][1], 0))
        while len(to_check):
            r, c, dist = to_check.popleft()
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                rr, cc = r + dr, c + dc
                if self.maze[rr, cc] == self.WALL:
                    continue
                elif (rr, cc) not in visited:
                    if self.maze[rr, cc] == self.KEY:
                        self.key_distances[(start, self.key_locations[(rr, cc)])] = dist + 1
                        self.key_distances[(self.key_locations[(rr, cc)], start)] = dist + 1
                    visited.add((rr, cc))
                    to_check.append((rr, cc, dist + 1))

    def detect_blocking(self, start):
        visited = set()
        visited.add(self.keys[start])
        to_check = deque()
        to_check.append((self.keys[start][0], self.keys[start][1], set()))
        while len(to_check):
            r, c, blockers = to_check.popleft()
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                rr, cc = r + dr, c + dc
                if self.maze[rr, cc] == self.WALL:
                    continue
                elif (rr, cc) not in visited:
                    if self.maze[rr, cc] == self.KEY:
                        self.blockers[(start, self.key_locations[(rr, cc)])] = blockers
                        visited.add((rr, cc))
                        to_check.append((rr, cc, blockers))
                    elif self.maze[rr, cc] == self.DOOR:
                        self.blockers[(start, self.door_locations[(rr, cc)])] = blockers
                        new_blockers = blockers.copy()
                        new_blockers.add(self.door_locations[(rr, cc)].lower())
                        visited.add((rr, cc))
                        to_check.append((rr, cc, new_blockers))
                    else:
                        visited.add((rr, cc))
                        to_check.append((rr, cc, blockers))

    def get_distance(self, current, keys, cache):
        if len(keys) == 0:  # no more keys to visit
            return 0
        if (current, str(keys)) in cache:
            return cache[(current, str(keys))]

        shortest = 9**9
        for target in keys:
            if len(self.blockers[(current, target)] & keys) == 0:  # not blocked
                new_keys = keys.copy()
                new_keys.remove(target)
                dist = self.key_distances[(current, target)] + self.get_distance(target, new_keys, cache)
                if dist < shortest:
                    shortest = dist

        cache[(current, str(keys))] = shortest
        return shortest

    def collect_all_keys(self):
        keys = list(self.keys.keys())
        for start in keys:
            self.measure_key_distances_from(start)
        for start in keys:
            self.detect_blocking(start)

        cache = {}
        keys = set(self.keys.keys())
        keys.remove("0")
        return self.get_distance("0", keys, cache)

    def get_distance_using_4_robots(self, current, keys, cache):
        if len(keys) == 0:  # no more keys to visit
            return 0
        if (str(current), str(keys)) in cache:
            return cache[(str(current), str(keys))]

        shortest = 9**9
        for target in keys:
            for robot in range(4):
                if (current[robot], target) not in self.key_distances:  # the robot can't reach the key
                    continue
                if len(self.blockers[(current[robot], target)] & keys) == 0:  # not blocked
                    new_keys = keys.copy()
                    new_keys.remove(target)
                    new_positions = current.copy()
                    new_positions[robot] = target
                    dist = self.key_distances[(current[robot], target)] + self.get_distance_using_4_robots(new_positions, new_keys, cache)
                    if dist < shortest:
                        shortest = dist

        cache[(str(current), str(keys))] = shortest
        return shortest

    def collect_all_keys_using_4_robots(self):
        cache = {}
        keys = set(self.keys.keys())
        keys.remove("1")
        keys.remove("2")
        keys.remove("3")
        keys.remove("4")
        return self.get_distance_using_4_robots(["1", "2", "3", "4"], keys, cache)


