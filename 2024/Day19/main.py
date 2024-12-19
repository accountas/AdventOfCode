from common.data import *
from time import time


def count_arrangements(target, towels):
    num_ways = [0] * (len(target) + 1)
    num_ways[0] = 1

    for idx in range(1, len(target) + 1):
        prefix = target[:idx]

        for towel in towels:
            if len(prefix) < len(towel):
                continue

            if prefix.endswith(towel):
                num_ways[idx] += num_ways[idx - len(towel)]

    return num_ways[-1]


def main():
    input = get_data(year=2024, day=19, sample=False)

    towels, targets = input.split("\n\n")
    towels = towels.split(", ")
    targets = targets.split("\n")

    counts = [count_arrangements(target, towels) for target in targets]

    print("Part 1:", sum(count > 0 for count in counts))
    print("Part 2:", sum(counts))


if __name__ == "__main__":
    start = time()
    main()
    print(f"Time: {time()-start:.4f} sec")
