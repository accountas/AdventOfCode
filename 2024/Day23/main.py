from common.data import *

from time import time
from collections import defaultdict
from itertools import combinations


def parse_input(input):
    graph = defaultdict(set)

    lines = input.splitlines()
    for line in lines:
        a, b = line.split("-")
        graph[a].add(b)
        graph[b].add(a)
    return graph


def subsets(iterable, max_size):
    if max_size is None:
        max_size = len(iterable)
    else:
        max_size = min(max_size, len(iterable))

    for size in range(max_size, 0, -1):
        for subset in combinations(iterable, size):
            yield subset


def is_clique(graph, nodes):
    return all(b in graph[a] for a, b in combinations(nodes, 2))


def find_cliques(graph, max_size=None, largest_only=False):
    cliques = set()

    for node in graph:
        for subset in subsets(graph[node], max_size):
            subset = set(subset) | {node}
            if is_clique(graph, subset):
                cliques.add(tuple(sorted(subset)))
                if largest_only:
                    break

    return cliques


def main():
    input = get_data(year=2024, day=23, sample=False)
    graph = parse_input(input)

    cliques = find_cliques(graph, max_size=3)
    triangles = sum(
        len(clique) == 3 and any(n[0] == "t" for n in clique) 
        for clique in cliques
    )
    print("Part 1:", triangles)

    cliques = find_cliques(graph, largest_only=True)
    largest = max(cliques, key=lambda x: len(x))
    print("Part 2:", ",".join(largest))


if __name__ == "__main__":
    start = time()
    main()
    print(f"Time: {time()-start:.4f} sec")
