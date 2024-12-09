from common.data import *
from tqdm import tqdm
from dataclasses import dataclass
from typing import Optional


@dataclass
class File:
    file_id: Optional[int]
    size: int
    was_moved: bool = False


def to_files(disk_map):
    return [
        File(file_id=idx // 2 if idx % 2 == 0 else None, size=int(size))
        for idx, size in enumerate(disk_map)
    ]


def to_blocks(files):
    blocks = []
    for file in files:
        blocks += [file.file_id] * file.size
    return blocks


def checksum(blocks):
    return sum(idx * file_id for idx, file_id in enumerate(blocks) if file_id != None)


# O(n * max_file_size)
def part_1(files): 
    blocks = to_blocks(files)
    left = 0
    right = len(blocks) - 1
    while left <= right:
        if blocks[left] != None:
            left += 1
        elif blocks[right] != None:
            blocks[left] = blocks[right]
            blocks[right] = None
            right -= 1
            left += 1
        else:
            right -= 1
    return checksum(blocks)

# O(n ^ 2) :(
def part_2(files):
    for i in tqdm(range(len(files) - 1, 0, -1)):
        file_to_move = files[i]

        if file_to_move.file_id is None or file_to_move.was_moved:
            continue

        file_to_move.was_moved = True

        for j in range(0, i):
            move_to = files[j]
            if move_to.file_id is None and move_to.size >= file_to_move.size:
                files[i] = File(None, file_to_move.size)
                remaining = File(None, move_to.size - file_to_move.size)
                files = files[:j] + [file_to_move, remaining] + files[j + 1 :]
                break

    return checksum(to_blocks(files))


def main():
    disk_map = get_data(year=2024, day=9, sample=False)
    files = to_files(disk_map)

    print(f"Part 1: {part_1(files)}")
    print(f"Part 2: {part_2(files)}")


if __name__ == "__main__":
    main()
