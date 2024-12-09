from common.data import *
from tqdm import tqdm
from dataclasses import dataclass
from typing import Optional


def add_ids(disk):
    return [(int(size), [None, idx // 2][idx % 2 == 0]) for idx, size in enumerate(disk)]

def decompact(data):
    full = []
    for i in data:
        full += [i[1]] * i[0]
    return full

def part_1(disk):
    disk = decompact(add_ids(disk))
    checksum = 0
    l = 0
    r = len(disk) - 1
    while l <= r:
        if disk[l] != None:
            checksum += l * disk[l]
            l += 1
        elif disk[r] != None:
            checksum += l * disk[r]
            r -= 1
            l += 1
        else:
            r -= 1
    return checksum


def part_2(disk):
    disk = add_ids(disk)

    for i in tqdm(range(len(disk) - 1, 0, -1)):
        if disk[i][1] is None or len(disk[i]) == 3:
            continue

        disk[i] = (disk[i][0], disk[i][1], True)

        for j in range(0, i):
            if disk[j][1] is None and disk[i][0] <= disk[j][0]:
                tmp = disk[i]
                disk[i] = (tmp[0], None)
                disk = disk[:j] + [tmp] + [(disk[j][0] - tmp[0], None)] + disk[j+1:]
    
    hash = 0
    for idx, file_id in enumerate(decompact(disk)):
        if file_id != None:
            hash += file_id * idx
    return hash

    
def main():
    input = get_data(year=2024, day=9, sample=False)
    print(f"N = {len(input)}")

    print(f"Part 1: {part_1(input)}")
    print(f"Part 2: {part_2(input)}")

if __name__ == "__main__":
    main()
