from common.data import *
from common.grid import *
from common.point import *


def dfs(pos, trail, visited):
    if visited != None and pos in visited:
        return 0

    if visited != None:
        visited.add(pos)

    if trail[pos] == 9:
        return 1

    reachable = 0
    for child in trail.neighbours(pos):
        if trail[child] == trail[pos] + 1:
            reachable += dfs(child, trail, visited)
    return reachable


def solve(trail):
    starts = trail.find(0)

    num_trail_heads = 0
    num_trails = 0
    for start in starts:
        num_trail_heads += dfs(start, trail, set())
        num_trails += dfs(start, trail, None)

    return num_trail_heads, num_trails


def main():
    input = get_data(year=2024, day=10, sample=False)

    trail = Grid.from_string(input)
    trail.map_values(int)

    part_1, part_2 = solve(trail)

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")


if __name__ == "__main__":
    main()
