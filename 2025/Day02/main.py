from common.data import *


def generate_invalid_ids(max_id, max_repetitions):
    invalid = set()
    for base in range(1, 10 ** (len(str(max_id)) // 2)):
        repetitions = 2
        while max_repetitions is None or max_repetitions >= repetitions:
            id = int(str(base) * repetitions)
            if id <= max_id:
                invalid.add(id)
            else:
                break
            repetitions += 1

    return invalid


def invalid_id_sum(ranges, max_repetitions):
    max_id = max(r for _, r in ranges)
    invalid_ids = generate_invalid_ids(max_id, max_repetitions)

    total = 0
    for l, r in ranges:
        for id in invalid_ids:
            if l <= id <= r:
                total += id
    return total


def main():
    # ranges = [
    #     list(map(int, r.split("-")))
    #     for r in get_data(year=2025, day=2, sample=True).split(",")
    # ]
    # print(f"Part 1:", invalid_id_sum(ranges, 2))
    # print(f"part 2:", invalid_id_sum(ranges, None))
    print(invalid_id_sum([[0, 10000000000]], None))


if __name__ == "__main__":
    main()
