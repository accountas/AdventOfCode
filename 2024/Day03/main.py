from common.data import *
import re


def part_1(data):
    pattern = r"mul\((\d{1,3},\d{1,3})\)"
    matches = [x.split(",") for x in re.findall(pattern, data)]
    return sum([int(x) * int(y) for x, y in matches])


def part_2(data):
    pattern = r"mul\((\d{1,3},\d{1,3})\)|(do)\(\)|(don't)\(\)"
    enabled = True
    ans = 0
    for match in re.findall(pattern, data):
        if match[1] == "do":
            enabled = True
        elif match[2] == "don't":
            enabled = False
        elif enabled:
            x, y = match[0].split(",")
            ans += int(x) * int(y)
    return ans


def main():
    data = get_data(year=2024, day=3, sample=False)

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")


if __name__ == "__main__":
    main()
