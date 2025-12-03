from common.data import *


def find_largest(bank, num_digits):
    if num_digits == 1:
        return max(bank)

    first_idx, first_digit = max(enumerate(bank[: -num_digits + 1]), key=lambda x: x[1])
    return first_digit + find_largest(bank[first_idx + 1 :], num_digits - 1)


def main():
    banks = get_data(year=2025, day=3, sample=False).splitlines()

    part1, part2 = 0, 0
    for bank in banks:
        part1 += int(find_largest(bank, 2))
        part2 += int(find_largest(bank, 12))

    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == "__main__":
    main()
