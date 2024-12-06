from common.data import *
from common.point import *
from common.grid import *
from tqdm import tqdm


def walk(grid, start_pos, start_dir):
    pos = start_pos
    dir = start_dir
    visited = set()
    loop = False
    while grid.is_valid(pos):
        if (pos, dir) in visited:
            loop = True
            break
        if not grid.is_valid(pos):
            break
        if grid[pos] != "#":
            visited.add((pos, dir))
            pos += dir
        elif grid[pos] == "#":
            pos -= dir
            dir = turn_right(dir)
            pos += dir
    visited_pos = set(pos for pos, _ in visited)
    return visited_pos, loop


def part_1(grid):
    start = grid.find("^")[0]
    visited, _ = walk(grid, start, UP)
    return len(visited)


def part_2(grid):
    start = grid.find("^")[0]
    visited, _ = walk(grid, start, UP)

    loops = 0
    for point in tqdm(visited, "Part 2 progress"):
        if grid[point] != ".":
            continue
        grid[point] = "#"
        _, loop = walk(grid, start, UP)
        loops += loop
        grid[point] = "."
    return loops


def main():
    input = get_data(year=2024, day=6, sample=False)
    grid = Grid.from_string(input)

    print(f"Part 1: {part_1(grid)}")
    print(f"Part 2: {part_2(grid)}")


if __name__ == "__main__":
    main()
