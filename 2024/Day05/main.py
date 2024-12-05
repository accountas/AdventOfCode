from common.data import *
from functools import cmp_to_key


def parse_data(data):
    lines = data.splitlines()
    constrains = set()
    updates = []
    for line in lines:
        if "|" in line:
            a, b = line.split("|")
            constrains.add((a, b))
        elif line != "":
            updates.append(line.split(","))

    return constrains, updates


def is_full_graph(constrains, update):
    # Sanity check
    for a, b in zip(update, update[1:]):
        if (a, b) not in constrains and (b, a) not in constrains:
            return False
    return True


def solve(constrains, updates):
    total_good = 0
    total_fixed = 0

    for update in updates:
        assert is_full_graph(constrains, update)
        fixed = sorted(update, key=cmp_to_key(lambda a, b: [1, -1][(a, b) in constrains]))
        middle = int(fixed[len(fixed) // 2])
        if fixed == update:
            total_good += middle
        else:
            total_fixed += middle

    return total_good, total_fixed


def main():
    input = get_data(year=2024, day=5, sample=True)
    graph, updates = parse_data(input)
    part_1, part_2 = solve(graph, updates)

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")


if __name__ == "__main__":
    main()
