from common.data import *
from common.point import *
from common.grid import *

import re
import math

from tqdm import tqdm


def parse_input(input):
    lines = input.splitlines()
    pattern = r"-?\d+"

    robots = []
    for line in lines:
        numbers = list(map(int, re.findall(pattern, line)))
        pos = Point(numbers[0], numbers[1])
        velocity = Point(numbers[2], numbers[3])
        robots.append((pos, velocity))

    return robots


def simulate(robots, steps, width, height):
    after = []
    for pos, velocity in robots:
        final_pos = pos + velocity * steps
        final_pos.x %= width
        final_pos.y %= height
        after.append((final_pos, velocity))

    return after


def count_quadrants(robots, width, height):
    quadrants = [0] * 4

    def side(pos, length):
        if pos < length // 2:
            return 0
        if pos > length // 2:
            return 1
        return None

    for pos, _ in robots:
        side_x = side(pos.x, width)
        side_y = side(pos.y, height)

        if side_x is not None and side_y is not None:
            quadrants[side_x + side_y * 2] += 1

    return quadrants


def print_state(robots, width, height):
    grid = Grid.empty(width, height, ".")
    for pos, _ in robots:
        grid[pos] = "#"
    print(grid)


def largest_blob(robots):
    occupied = set(pos for pos, _ in robots)
    visited = set()

    def dfs(pos):
        if pos in visited or pos not in occupied:
            return 0

        visited.add(pos)
        return 1 + sum(dfs(pos + dir) for dir in DIRECTIONS)

    biggest = 0
    for pos, _ in robots:
        biggest = max(biggest, dfs(pos))

    return biggest


def main():
    input = get_data(year=2024, day=14, sample=False)
    robots = parse_input(input)
    width, height = 101, 103

    part_1 = math.prod(count_quadrants(simulate(robots, 100, width, height), width, height))
    part_2 = None

    for steps in tqdm(range(0, 10000)):
        after = simulate(robots, steps, width, height)
        if largest_blob(after) > 50:
            print_state(after, width, height)
            part_2 = steps
            break

    print("part 1", part_1)
    print("part 2", part_2)


if __name__ == "__main__":
    main()
