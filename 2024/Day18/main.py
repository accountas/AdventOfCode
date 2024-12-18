from common.data import *
from common.point import *
from common.grid import *
from collections import deque
from tqdm import tqdm


class DSU:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
        elif self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        if self.rank[x] < self.rank[y]:
            x, y = y, x

        self.parent[y] = x
        if self.rank[x] == self.rank[y]:
            self.rank[x] += 1

    def connected(self, x, y):
        return self.find(x) == self.find(y)


def parse_input(input):
    return [Point(*list(map(int, line.split(",")[::-1]))) for line in input.splitlines()]


def shortest_path(grid, start, end):
    queue = deque([start])
    dist = {start: 0}

    while queue:
        current = queue.popleft()
        if current == end:
            break

        for neighbor in grid.neighbours(current):
            if neighbor not in dist and grid[neighbor]:
                dist[neighbor] = dist[current] + 1
                queue.append(neighbor)

    return dist.get(end)


def main():
    input = get_data(year=2024, day=18, sample=False)
    points = parse_input(input)

    start = Point(0, 0)
    end = Point(70, 70)
    grid = Grid.empty(71, 71, True)
    fall_first = 1024

    # ====== PART 1 ======
    for point in points[:fall_first]:
        grid[point] = False

    print("Part 1:", shortest_path(grid, start, end))

    # ====== PART 2 ======
    for point in points[fall_first:]:
        grid[point] = False

    dsu = DSU()

    def add_point(point):
        for neighbor in grid.neighbours(point):
            if grid[neighbor]:
                dsu.union(point, neighbor)

    for point in grid.find(True):
        add_point(point)

    for point in reversed(points):
        grid[point] = True
        add_point(point)
        if dsu.connected(start, end):
            break

    print(f"Part 2: {point.j},{point.i}")


if __name__ == "__main__":
    main()
