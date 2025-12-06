from common.data import *
from common.grid import *
from common.point import *


def parse_input(input):
    lines = input.splitlines()
    line_length = len(lines[0])

    separator_indexes = [-1]
    for column in range(line_length):
        all_empty = all(l[column] == " " for l in lines)
        if all_empty:
            separator_indexes.append(column)
    separator_indexes.append(line_length)

    problems = []
    for left, right in zip(separator_indexes, separator_indexes[1:]):
        problem = []
        for line in lines[:-1]:
            problem.append(line[left + 1 : right])
        problems.append(problem)

    operations = lines[-1].split()
    return problems, operations


def part_1(problems, operations):
    total = 0
    for numbers, operator in zip(problems, operations):
        total += eval(operator.join(numbers))
    return total


def part_2(problems, operations):
    total = 0
    for numbers, operator in zip(problems, operations):
        transposed = list(map("".join, zip(*numbers)))
        total += eval(operator.join(transposed))
    return total


def main():
    lines = get_data(year=2025, day=6, sample=True)
    problems, operations = parse_input(lines)

    print("Part 1:", part_1(problems, operations))
    print("Part 2:", part_2(problems, operations))


if __name__ == "__main__":
    main()
