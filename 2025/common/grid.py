from common.point import *

UP = Point(-1, 0)
DOWN = Point(1, 0)
LEFT = Point(0, -1)
RIGHT = Point(0, 1)
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

UP_LEFT = UP + LEFT
UP_RIGHT = UP + RIGHT
DOWN_LEFT = DOWN + LEFT
DOWN_RIGHT = DOWN + RIGHT
DIAGONALS = [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
ALL_DIRECTIONS = [UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT]

def turn_right(direction, dirs=DIRECTIONS):
    return dirs[(dirs.index(direction) + 1) % len(dirs)]

def turn_left(direction, dirs=DIRECTIONS):
    return dirs[(dirs.index(direction) - 1) % len(dirs)]


class Grid:
    def __init__(self, values):
        self.values = values
        self.n = len(values)
        self.m = len(values[0]) if hasattr(values[0], "__len__") else 0

    @classmethod
    def from_string(cls, input):
        values = [list(line) for line in input.splitlines()]
        return cls(values)
    
    @classmethod
    def empty(cls, n, m, value=None):
        return cls([[value for _ in range(m)] for _ in range(n)])

    def is_valid(self, point):
        return 0 <= point[0] < self.n and 0 <= point[1] < self.m

    def neighbours(self, point, directions=DIRECTIONS):
        if not isinstance(point, Point):
            point = Point(*point)

        for direction in directions:
            new_point = point + direction
            if self.is_valid(new_point):
                yield new_point

    def neighbour_values(self, point, directions=DIRECTIONS):
        for idx in self.neigbor_idxs(point, directions):
            yield self[idx]

    def pos_iter(self):
        for i in range(self.n):
            for j in range(self.m):
                yield Point(i, j)

    def items(self):
        for point in self.pos_iter():
            yield point, self[point]
    
    def find(self, value):
        found = []
        for point in self.pos_iter():
            if self[point] == value:
                found.append(point)
        return found
    
    def map_values(self, fn):
        for point in self.pos_iter():
            self[point] = fn(self[point])

    def swap(self, a, b):
        self[a], self[b] = self[b], self[a]

    def __repr__(self):
        return "\n".join(" ".join(map(str,row)) for row in self.values)

    def __getitem__(self, idx):
        if isinstance(idx, (tuple, Point)):
            if self.is_valid(idx):
                return self.values[idx[0]][idx[1]]
            return None
        return self.values[idx]
    
    def __setitem__(self, idx, value):
        self.values[idx[0]][idx[1]] = value
