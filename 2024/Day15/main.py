from common.data import *
from common.point import *
from common.grid import *

from copy import deepcopy


def parse_input(input):
    grid, moves = input.split("\n\n")
    grid = Grid.from_string(grid)
    dirs = {"^": UP, "v": DOWN, ">": RIGHT, "<": LEFT}
    moves = [dirs[move] for move in moves.replace("\n", "")]

    return grid, moves


def make_simple_move(grid, pos, direction):
    new_pos = pos + direction

    if grid[new_pos] == "#":
        return pos

    if grid[new_pos] == ".":
        grid[pos], grid[new_pos] = grid[new_pos], grid[pos]
        return new_pos

    if make_simple_move(grid, new_pos, direction) == new_pos:
        return pos
    else:
        grid[pos], grid[new_pos] = grid[new_pos], grid[pos]
        return new_pos


def can_push(grid, pos, direction):
    boxes = [pos]
    if grid[pos] == "]":
        boxes.append(pos + Point(0, -1))
    elif grid[pos] == "[":
        boxes.append(pos + Point(0, 1))
    else:
        assert False, "not a box"

    can = True
    for box in boxes:
        new_pos = box + direction
        if grid[new_pos] == "#":
            return False
        if grid[box] == grid[new_pos]:
            return can_push(grid, new_pos, direction)
        else:
            can &= grid[new_pos] == "." or can_push(grid, new_pos, direction)

    return can


def push_boxes(grid, pos, direction):
    boxes = [pos]
    if grid[pos] == "]":
        boxes.append(pos + Point(0, -1))
    elif grid[pos] == "[":
        boxes.append(pos + Point(0, 1))
    else:
        assert False, "not a box"

    for box in boxes:
        new_pos = box + direction
        if grid[new_pos] == grid[box]:
            push_boxes(grid, new_pos, direction)
            break
        if grid[new_pos] in ("[", "]"):
            push_boxes(grid, new_pos, direction)

    for box in boxes:
        grid[box], grid[box + direction] = grid[box + direction], grid[box]


def make_vertical_move(grid, pos, direction):
    new_pos = pos + direction

    if grid[new_pos] == "#":
        return pos

    if grid[new_pos] == ".":
        grid[pos], grid[new_pos] = grid[new_pos], grid[pos]
        return new_pos

    if grid[new_pos] in ("[", "]"):
        if can_push(grid, new_pos, direction):
            push_boxes(grid, new_pos, direction)
            grid[pos], grid[new_pos] = grid[new_pos], grid[pos]
            return new_pos
        else:
            return pos


def sum_boxes(grid, box_type):
    total = 0
    for box in grid.find(box_type):
        total += box.j + box.i * 100

    return total


def expand_grid(grid):
    new_grid = Grid.empty(grid.n, grid.m * 2, ".")

    for pos, value in grid.items():
        pos = Point(pos.i, pos.j * 2)

        if value == "@":
            new_grid[pos] = "@"
        if value == "O":
            new_grid[pos] = "["
            new_grid[pos + Point(0, 1)] = "]"
        if value == "#":
            new_grid[pos] = "#"
            new_grid[pos + Point(0, 1)] = "#"

    return new_grid


def part_1(grid, moves):
    grid = deepcopy(grid)
    pos = grid.find("@")[0]
    for move in moves:
        pos = make_simple_move(grid, pos, move)
    return sum_boxes(grid, "O")


def part_2(grid, moves):
    grid = deepcopy(grid)
    grid = expand_grid(grid)
    pos = grid.find("@")[0]
    for move in moves:
        if move.i != 0:
            pos = make_vertical_move(grid, pos, move)
        else:
            pos = make_simple_move(grid, pos, move)
    return sum_boxes(grid, "[")


def main():
    input = get_data(year=2024, day=15, sample=False)
    grid, moves = parse_input(input)

    print(f"Part 1: {part_1(grid, moves)}")
    print(f"Part 2: {part_2(grid, moves)}")


if __name__ == "__main__":
    main()
