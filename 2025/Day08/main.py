from common.data import *
from common.utils import time_it
import itertools as it


class DSU:
    def __init__(self, nodes):
        self._parent = {node: node for node in nodes}
        self._size = {node: 1 for node in nodes}
        self.num_components = len(nodes)

    def root(self, node):
        if self._parent[node] == node:
            return node

        self._parent[node] = self.root(self._parent[node])
        return self._parent[node]

    def union(self, a, b):
        root_a = self.root(a)
        root_b = self.root(b)

        if root_a != root_b:
            if self._size[root_a] < self._size[root_b]:
                a, b = b, a

            self._parent[root_b] = root_a
            self._size[root_a] += self._size[root_b]
            self.num_components -= 1

    def connected(self, a, b):
        return self.root(a) == self.root(b)

    def sizes(self):
        return [size for node, size in self._size.items() if self._parent[node] == node]


def distance_squared(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def main():
    sample = False
    data = get_data(year=2025, day=8, sample=sample).splitlines()
    boxes = [tuple(map(int, line.split(","))) for line in data]

    part_1_limit = 10 if sample else 1000

    dsu = DSU(boxes)

    edges = []
    for a, b in it.combinations(boxes, 2):
        edges.append((distance_squared(a, b), a, b))
    edges.sort()

    for idx, (_, a, b) in enumerate(edges):
        if not dsu.connected(a, b):
            dsu.union(a, b)
            if dsu.num_components == 1:
                print("Part 2:", a[0] * b[0])
                break
        if idx == part_1_limit - 1:
            group_sizes = sorted(dsu.sizes(), reverse=True)
            print("Part 1:", group_sizes[0] * group_sizes[1] * group_sizes[2])


if __name__ == "__main__":
    time_it(main)
