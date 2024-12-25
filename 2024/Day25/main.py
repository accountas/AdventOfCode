from common.data import *
from common.grid import *
from common.point import *
from itertools import product
from time import time


def parse_input(input):
    raw_locks = [Grid.from_string(s) for s in input.split("\n\n")]

    locks = []
    keys = []

    for lock in raw_locks:
        heights = [0] * lock.m
        for point in lock.find("#"):
            heights[point.j] += 1
        if lock[0, 0] == "#":
            locks.append(heights)
        else:
            keys.append(heights)

    return locks, keys


def main():
    input = get_data(year=2024, day=25, sample=False)
    locks, keys = parse_input(input)

    matches = sum(
        all(lock_pin + key_pin <= 7 for lock_pin, key_pin in zip(lock, key))
        for lock, key in product(locks, keys)
    )

    print("Result:", matches)


if __name__ == "__main__":
    start = time()
    main()
    print(f"Time: {time()-start:.4f} sec")
