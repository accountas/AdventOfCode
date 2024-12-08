from common.data import *
from common.grid import *
from common.point import *
from collections import defaultdict
from itertools import combinations


def find_antennas(grid):
    antennas = defaultdict(set)

    for point, value in grid.items():
        if value != ".":
            antennas[value].add(point)

    return antennas


def find_antinodes_p1(a, b, grid):
    antinodes = set()
    diff = a - b
    a += diff
    b -= diff
    if grid.is_valid(a):
        antinodes.add(a)
    if grid.is_valid(b):
        antinodes.add(b)
    return antinodes


def find_antinodes_p2(a, b, grid):
    antinodes = set()
    diff = a - b
    while grid.is_valid(a) or grid.is_valid(b):
        if grid.is_valid(a):
            antinodes.add(a)
        if grid.is_valid(b):
            antinodes.add(b)
        a += diff
        b -= diff
    return antinodes


def solve(antennas, grid):
    antinodes_p1 = set()
    antinodes_p2 = set()

    for pos in antennas.values():
        for a, b in combinations(pos, 2):
            antinodes_p1 |= find_antinodes_p1(a, b, grid)
            antinodes_p2 |= find_antinodes_p2(a, b, grid)

    return len(antinodes_p1), len(antinodes_p2)


def main():
    input = get_data(year=2024, day=8, sample=False)
    grid = Grid.from_string(input)
    antennas = find_antennas(grid)
    part_1, part_2 = solve(antennas, grid)

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")


if __name__ == "__main__":
    main()
