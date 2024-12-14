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


def quadrant_score(robots, width, height):
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

    return math.prod(quadrants)


def print_state(robots, width, height):
    grid = Grid.empty(height, width, ".")
    for pos, _ in robots:
        grid[pos.y, pos.x] = "#"
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
    max_iterations = 20000

    print("Part 1:", quadrant_score(simulate(robots, 10000, width, height), width, height))

    for steps in tqdm(range(max_iterations), "Part 2, blob size"):
        after = simulate(robots, steps, width, height)
        if largest_blob(after) > 50:
            print_state(after, width, height)
            part_2 = steps
            break

    print("Part 2:", part_2)

    # Alternative solution, small part 1 score = quadrants unevenly distributed
    # A lot faster than the above solution
    min_quadrant_score = (1e9, None)
    for steps in tqdm(range(max_iterations), "Part 2, min quadrant score"):
        after = simulate(robots, steps, width, height)
        score = quadrant_score(after, width, height)
        min_quadrant_score = min(min_quadrant_score, (score, steps))

    print_state(simulate(robots, min_quadrant_score[1], width, height), width, height)
    print("Part 2:", part_2)


if __name__ == "__main__":
    main()
