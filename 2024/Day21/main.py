from common.data import *
from common.point import *

from time import time
from functools import cache


"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""
DIR_PAD = {
    Point(0, 1): "^",
    Point(0, 2): "A",
    Point(1, 0): "<",
    Point(1, 1): "v",
    Point(1, 2): ">",
}

"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""
NUM_PAD = {
    Point(0, 0): "7",
    Point(0, 1): "8",
    Point(0, 2): "9",
    Point(1, 0): "4",
    Point(1, 1): "5",
    Point(1, 2): "6",
    Point(2, 0): "1",
    Point(2, 1): "2",
    Point(2, 2): "3",
    Point(3, 1): "0",
    Point(3, 2): "A",
}

DIRECTIONS = {
    Point(-1, 0): "^",
    Point(1, 0): "v",
    Point(0, -1): "<",
    Point(0, 1): ">",
}


@cache
def dir_pad_paths(start, end):
    dir_pad_inv = invert_dict(DIR_PAD)
    start = dir_pad_inv[start]
    end = dir_pad_inv[end]
    return list(all_paths(start, end, DIR_PAD))


@cache
def num_pad_paths(start, end):
    num_pad_inv = invert_dict(NUM_PAD)
    start = num_pad_inv[start]
    end = num_pad_inv[end]
    return list(all_paths(start, end, NUM_PAD))


def invert_dict(d):
    return {v: k for k, v in d.items()}


def all_paths(now, target, pad, visited=set(), path=[]):
    if now in visited:
        return

    if now == target:
        yield path

    for dir, dir_name in DIRECTIONS.items():
        new_pos = now + dir
        if new_pos in pad:
            yield from all_paths(
                new_pos, target, pad, visited | {now}, path + [dir_name]
            )


@cache
def num_pad_cost(start, end, num_robots):
    best = float("inf")
    for path in num_pad_paths(start, end):
        path = ["A"] + path + ["A"]
        best = min(
            best, sum(dir_pad_cost(a, b, num_robots) for a, b in zip(path, path[1:]))
        )
    return best


@cache
def dir_pad_cost(start, end, num_left):
    if num_left == 0:
        return 1

    best = float("inf")
    for path in dir_pad_paths(start, end):
        path = ["A"] + path + ["A"]
        best = min(
            best, sum(dir_pad_cost(a, b, num_left - 1) for a, b in zip(path, path[1:]))
        )
    return best


def solve(pins, num_robots):
    ans = 0
    for pin in pins:
        for a, b in zip("A" + pin, pin):
            cost = num_pad_cost(a, b, num_robots)
            ans += cost * int(pin[:-1])
    return ans


def main():
    pins = get_data(year=2024, day=21, sample=False).splitlines()

    print("Part 1:", solve(pins, 2))
    print("Part 2:", solve(pins, 25))


if __name__ == "__main__":
    start = time()
    main()
    print(f"Time: {time()-start:.4f} sec")
