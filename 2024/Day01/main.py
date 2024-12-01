from collections import Counter
from common.data import *


def parse_data(data):
    lines = data.splitlines()
    list_a = []
    list_b = []
    for line in lines:
        a, b = line.split()
        list_a.append(int(a))
        list_b.append(int(b))

    return list_a, list_b


def part_1(list_a, list_b):
    return sum(abs(a - b) for a, b in zip(sorted(list_a), sorted(list_b)))


def part_2(list_a, list_b):
    list_b_counter = Counter(list_b)
    return sum(a * list_b_counter[a] for a in list_a)


def main():
    data = get_data(year=2024, day=1, sample=False)
    parsed = parse_data(data)

    print(f"Part 1: {part_1(*parsed)}")
    print(f"Part 2: {part_2(*parsed)}")


if __name__ == "__main__":
    main()
