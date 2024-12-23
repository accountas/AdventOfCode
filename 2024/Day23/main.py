from common.data import *

from time import time
from collections import defaultdict
from itertools import combinations
from random import shuffle


def parse_input(input):
    graph = defaultdict(set)
    lines = input.splitlines()
    shuffle(lines)
    for line in lines:
        a, b = line.split("-")
        graph[a].add(b)
        graph[b].add(a)
    return graph


def count_triangles(graph):
    trianges = set(
        tuple(sorted([a, b, c]))
        for a in graph if a[0] == "t"
        for b in graph[a]
        for c in graph[b] if c in graph[a]
    )
    return len(trianges)


def max_clique(graph):
    best = set()

    def subsets(nodes):
        for size in range(len(nodes), 0, -1):
            for subset in combinations(nodes, size):
                yield subset

    def is_clique(nodes):
        return all(b in graph[a] for a, b in combinations(nodes, 2))

    for node in graph:
        for subset in subsets(graph[node]):
            subset = set(subset) | {node}
            if len(subset) <= len(best):
                break
            if is_clique(subset):
                best = subset

    return ",".join(sorted(best))


def main():
    input = get_data(year=2024, day=23, sample=False)
    graph = parse_input(input)

    print("Part 1:", count_triangles(graph))
    print("Part 2:", max_clique(graph))


if __name__ == "__main__":
    start = time()
    main()
    print(f"Time: {time()-start:.4f} sec")
