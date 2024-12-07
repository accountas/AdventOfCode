from common.data import *


def parse_input(input):
    equations = []
    for line in input.splitlines():
        target, values = line.split(": ")
        target = int(target)
        values = list(map(int, values.split()))
        equations.append((target, values))
    return equations


def brute_force(target, current, remaining, operators):
    if not remaining:
        return current == target
    if current > target:
        return False
    return any(
        brute_force(target, op(current, remaining[0]), remaining[1:], operators)
        for op in operators
    )


def sum_correct_targets(equations, operators):
    return sum(
        target * brute_force(target, values[0], values[1:], operators)
        for target, values in equations
    )


def part_1(equations):
    operators = [lambda x, y: x + y, lambda x, y: x * y]
    return sum_correct_targets(equations, operators)


def part_2(equations):
    operators = [
        lambda x, y: x + y,
        lambda x, y: x * y,
        lambda x, y: int(str(x) + str(y)),
    ]
    return sum_correct_targets(equations, operators)


def main():
    input = get_data(year=2024, day=7, sample=True)
    equations = parse_input(input)

    print(f"Part 1: {part_1(equations)}")
    print(f"Part 2: {part_2(equations)}")


if __name__ == "__main__":
    main()
