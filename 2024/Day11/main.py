from common.data import *
from copy import copy
from collections import defaultdict


def simulate(stones, steps):
    stone_counts = defaultdict(lambda: 0)

    for stone in stones:
        stone_counts[stone] += 1

    for _ in range(steps):
        new_stone_counts = defaultdict(lambda: 0)

        for stone, count in stone_counts.items():
            if stone == 0:
                new_stone_counts[1] += count
            elif stone >= 10 and len(str(stone)) % 2 == 0:
                stone_a = int(str(stone)[: len(str(stone)) // 2])
                stone_b = int(str(stone)[len(str(stone)) // 2 :])

                new_stone_counts[stone_a] += count
                new_stone_counts[stone_b] += count
            else:
                new_stone_counts[stone * 2024] += count

        stone_counts = copy(new_stone_counts)

    return sum(stone_counts.values())


def main():
    input = get_data(year=2024, day=11, sample=False)
    stones = list(map(int, input.split()))

    print(f"Part 1: {simulate(stones, 25)}")
    print(f"Part 2: {simulate(stones, 75)}")


if __name__ == "__main__":
    main()
