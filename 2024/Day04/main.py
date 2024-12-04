from common.data import *
from common.point import *
from common.grid import *

def part_1(grid: Grid):
    total = 0
    for point in grid.pos_iter():
        for dir in [LEFT, DOWN, DOWN_LEFT, DOWN_RIGHT]:
            indexes = [point + dir * x for x in range(4)]
            if all(grid.is_valid(p) for p in indexes):
                word = "".join([grid[p] for p in indexes])
                total += word == "XMAS" or word == "SAMX"

    return total


def part_2(grid: Grid):
    total = 0
    for point in grid.pos_iter():
        offsets = [Point(0, 0), Point(0, 2), Point(1, 1), Point(2, 0), Point(2, 2)]
        indexes = [point + offset for offset in offsets]
        if all(grid.is_valid(p) for p in indexes):
            word = "".join([grid[p] for p in indexes])
            total += word in ["MSAMS", "SSAMM", "MMASS", "SMASM"]

    return total


def main():
    input = get_data(year=2024, day=4, sample=False)
    grid = Grid.from_string(input)

    print(f"Part 1: {part_1(grid)}")
    print(f"Part 2: {part_2(grid)}")


if __name__ == "__main__":
    main()
