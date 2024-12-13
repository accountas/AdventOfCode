from common.data import *
from common.grid import *
from common.point import *
from collections import defaultdict
import re
from functools import cache
from tqdm import tqdm
from fractions import Fraction

INF = 10**9


def parse_input(input):
    lines = input.splitlines()

    machines = []
    n = len(lines) // 4 + (len(lines) % 4 != 0)
    for i in range(n):
        pattern_a = r"Button A: X\+([0-9]+), Y\+([0-9]+)"
        pattern_b = r"Button B: X\+([0-9]+), Y\+([0-9]+)"
        pattern_prize = r"Prize: X=([0-9]+), Y=([0-9]+)"

        a = Point(*map(int, re.findall(pattern_a, lines[i * 4])[0]))
        b = Point(*map(int, re.findall(pattern_b, lines[i * 4 + 1])[0]))
        prize = Point(*map(int, re.findall(pattern_prize, lines[i * 4 + 2])[0]))
        machines.append((a, b, prize))

    return machines


def solve(a, b, prize):
    """
    ax * x + bx * y = prize_x
    ay * x + by * y = prize_y

    x = (prize_x - bx * y) / ax
    ay * (prize_x - bx * y) / ax + by * y = prize_y
    ay * prize_x / ax - ay * bx * y / ax + by * y = prize_y
    ay * prize_x / ax + (by - ay * bx / ax) * y = prize_y
    y = (prize_y - ay * prize_x / ax) / (by - ay * bx / ax)

    Will fail if buttons are colinear
    """

    ax = Fraction(a.x)
    ay = Fraction(a.y)
    bx = Fraction(b.x)
    by = Fraction(b.y)
    prize_x = Fraction(prize.x)
    prize_y = Fraction(prize.y)

    y = (prize_y - ay * prize_x / ax) / (by - ay * bx / ax)
    x = (prize_x - bx * y) / ax

    if x.denominator != 1 or y.denominator != 1:
        return 0

    return x.numerator * 3 + y.numerator


def main():
    input = get_data(year=2024, day=13, sample=False)
    machines = parse_input(input)

    part_1 = 0
    for a, b, prize in machines:
        part_1 += solve(a, b, prize)

    part_2 = 0
    for a, b, prize in machines:
        part_2 += solve(a, b, prize + Point(10000000000000, 10000000000000))

    print("Part 1:", part_1)
    print("Part 2:", part_2)


if __name__ == "__main__":
    main()
