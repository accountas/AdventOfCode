from common.data import *
from common.utils import time_it
from functools import cache


def main():
    # Assumes input is a DAG
    data = get_data(year=2025, day=11, sample=False)
    graph = {t[0][:-1]: t[1:] for line in data.splitlines() if (t := line.split())}

    @cache
    def path_count(start_node, end_node, need):
        if start_node == end_node:
            return 1 if len(need) == 0 else 0

        if start_node in need:
            need = tuple(n for n in need if n != start_node)

        total = 0
        for child in graph[start_node]:
            total += path_count(child, end_node, need)
        return total

    print("Part 1:", path_count("you", "out", ()))
    print("Part 2:", path_count("svr", "out", ("fft", "dac")))


if __name__ == "__main__":
    time_it(main)
