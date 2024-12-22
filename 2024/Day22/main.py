from common.data import *
from common.point import *
from common.grid import *

from time import time
from functools import cache
from collections import defaultdict, deque
from tqdm import tqdm


def get_next(number):
    mod = 16777216
    number ^= number * 64
    number %= mod

    number ^= number // 32
    number %= mod

    number ^= number * 2048
    number %= mod

    return number


def part_1(seeds):
    ans = 0
    for seed in seeds:
        for _ in range(2000):
            seed = get_next(seed)
        ans += seed
    return ans


def part_2(seeds):
    N = len(seeds)

    deltas = [[] for _ in range(N)]
    ask_prices = [[] for _ in range(N)]

    for monkey_idx, seed in enumerate(seeds):
        for _ in range(2000):
            before = seed % 10
            seed = get_next(seed)
            now = seed % 10
            deltas[monkey_idx].append(now - before)
            ask_prices[monkey_idx].append(now)

    firsts = defaultdict(dict)

    for monkey_idx in range(len(seeds)):
        for idx in range(3, len(deltas[monkey_idx])):
            diff = tuple(deltas[monkey_idx][idx - 3 : idx + 1])
            sell_value = ask_prices[monkey_idx][idx]

            if monkey_idx not in firsts[diff]:
                firsts[diff][monkey_idx] = sell_value

    best = 0
    for diff, firsts in firsts.items():
        best = max(best, sum(firsts.values()))

    return best


def main():
    seeds = get_data(year=2024, day=22, sample=False).splitlines()
    seeds = list(map(int, seeds))

    print("Part 1:", part_1(seeds))
    print("Part 2:", part_2(seeds))


if __name__ == "__main__":
    start = time()
    main()
    print(f"Time: {time()-start:.4f} sec")
