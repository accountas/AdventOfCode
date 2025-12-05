from common.data import *


def merge_ranges(ranges):
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]
    for l, r in sorted_ranges[1:]:
        if l <= merged[-1][1]:
            merged[-1][1] = max(r, merged[-1][1])
        else:
            merged.append([l, r])
    return merged


def part1(ranges, ingredients):
    spoiled = 0
    for ingredient in ingredients:
        for l, r in ranges:
            if l <= ingredient <= r:
                spoiled += 1
                break
    return spoiled


def part2(ranges):
    return sum(r - l + 1 for l, r in ranges)


def main():
    ranges, ingredients = get_data(year=2025, day=5, sample=False).split("\n\n")

    ranges = [list(map(int, r.split("-"))) for r in ranges.splitlines()]
    ingredients = [int(line) for line in ingredients.splitlines()]

    merged_ranges = merge_ranges(ranges)

    print("Part 1:", part1(merged_ranges, ingredients))
    print("Part 2:", part2(merged_ranges))


if __name__ == "__main__":
    main()
