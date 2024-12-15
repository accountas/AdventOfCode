from common.data import *
from common.point import *
from common.grid import *


def make_move(grid, pos, direction):
    new_pos = pos + direction

    if grid[new_pos] == "#":
        return pos

    if grid[new_pos] == ".":
        grid.swap(pos, new_pos)
        return new_pos

    if grid[new_pos] in "O[]" and maybe_push_boxes(grid, new_pos, direction):
        grid.swap(pos, new_pos)
        return new_pos

    return pos


def maybe_push_boxes(grid, pushed_box, direction):
    adj_boxes = set()

    def find_boxes(pos):
        if pos in adj_boxes:
            return
        if grid[pos] == "]":
            adj_boxes.add(pos)
            find_boxes(pos + Point(0, -1))
            find_boxes(pos + direction)
        elif grid[pos] == "[":
            adj_boxes.add(pos)
            find_boxes(pos + Point(0, 1))
            find_boxes(pos + direction)
        elif grid[pos] == "O":
            adj_boxes.add(pos)
            find_boxes(pos + direction)

    find_boxes(pushed_box)

    for box in adj_boxes:
        if grid[box + direction] == "#":
            return False

    # Sorting by the decreasing distance (in one direction) to the pushed box
    for box in sorted(adj_boxes, key=lambda box: box * direction, reverse=True):
        grid.swap(box, box + direction)

    return True


def sum_boxes(grid, box_type):
    return sum(b.i * 100 + b.j for b in grid.find(box_type))


def expand_grid(raw_grid):
    return (
        raw_grid
            .replace(".", "..")
            .replace("#", "##")
            .replace("O", "[]")
            .replace("@", "@.")
    )


def simulate(grid, moves):
    pos = grid.find("@")[0]
    for move in moves:
        pos = make_move(grid, pos, move)


def main():
    input = get_data(year=2024, day=15, sample=False)
    raw_grid, raw_moves = input.split("\n\n")

    directions = {"^": UP, "v": DOWN, "<": LEFT, ">": RIGHT}
    moves = [directions[move] for move in raw_moves if move != "\n"]

    grid = Grid.from_string(raw_grid)
    simulate(grid, moves)
    print(f"Part 1: {sum_boxes(grid, "O")}")

    expanded_grid = Grid.from_string(expand_grid(raw_grid))
    simulate(expanded_grid, moves)
    print(f"Part 2: {sum_boxes(expanded_grid, "[")}")


if __name__ == "__main__":
    main()
