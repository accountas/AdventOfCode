from common.data import *


def parse_data(data):
    lines = data.splitlines()
    return [list(map(int, line.split())) for line in lines]


def is_safe(line):
    def increasing(line):
        for idx in range(1, len(line)):
            if not (1 <= line[idx - 1] - line[idx] <= 3):
                return False
        return True

    return increasing(line) or increasing(line[::-1])


def part_1(lines):
    return sum(map(is_safe, lines))


def part_2(lines):
    total = 0
    for line in lines:
        total += any(is_safe(line[:idx] + line[idx + 1 :]) for idx in range(len(line)))
    return total


def main():
    data = get_data(year=2024, day=2, sample=False)
    parsed = parse_data(data)

    print(f"Part 1: {part_1(parsed)}")
    print(f"Part 2: {part_2(parsed)}")


if __name__ == "__main__":
    main()
