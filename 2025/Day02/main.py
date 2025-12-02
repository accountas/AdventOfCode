from common.data import *

def invalid_ids_for_range(range_start, range_end, max_repetitions):
    invalid = set()
    for base in range(1, 10 ** (len(str(range_end)) // 2)):
        repetitions = 2
        while max_repetitions is None or max_repetitions >= repetitions:
            id = int(str(base) * repetitions)
            if id >= range_start and id <= range_end:
                invalid.add(id)
            elif id > range_end:
                break
            repetitions += 1
    return invalid

def main():
    ranges = [
        list(map(int, r.split("-")))
        for r in get_data(year=2025, day=2, sample=False).split(",")
    ]
    
    part_1 = 0
    part_2 = 0

    for range_start, range_end in ranges:
        # Assuming ranges don't intersect
        part_1 += sum(invalid_ids_for_range(range_start, range_end, 2))
        part_2 += sum(invalid_ids_for_range(range_start, range_end, None))

    print(f"Part 1:", part_1)
    print(f"part 2:", part_2)

if __name__ == "__main__":
    main()
    