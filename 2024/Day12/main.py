from common.data import *
from common.grid import *
from common.point import *
from collections import defaultdict


def fill_plot(pos, garden, plant_type, plot_id, visited):
    if pos in visited:
        return 0, 0

    area = 1
    perimeter = 4 - len(list(garden.neighbours(pos)))

    garden[pos] = plot_id
    visited.add(pos)

    for child in garden.neighbours(pos):
        if garden[child] == plant_type:
            result = fill_plot(child, garden, plant_type, plot_id, visited)
            area += result[0]
            perimeter += result[1]
        elif garden[child] != plot_id:
            perimeter += 1

    return area, perimeter


def compute_sides(garden):
    # Scan dir, step dir, side dir
    dirs = [
        (RIGHT, DOWN, UP),
        (RIGHT, DOWN, DOWN),
        (DOWN, RIGHT, LEFT),
        (DOWN, RIGHT, RIGHT),
    ]

    perimeters = defaultdict(lambda: 0)
    for scan_dir, step_dir, side_dir in dirs:
        cur_pos = Point(0, 0)
        while garden.is_valid(cur_pos):
            plant_last = garden[cur_pos]
            is_side_last = garden[cur_pos] != garden[cur_pos + side_dir]
            next_line_start = cur_pos + step_dir

            while garden.is_valid(cur_pos):
                cur_pos += scan_dir
                plant_now = garden[cur_pos]
                is_side_now = garden[cur_pos] != garden[cur_pos + side_dir]

                if is_side_last and (plant_last != plant_now or not is_side_now):
                    perimeters[plant_last] += 1

                plant_last, is_side_last = plant_now, is_side_now
            cur_pos = next_line_start
    return perimeters


def main():
    input = get_data(year=2024, day=12, sample=False)
    garden = Grid.from_string(input)

    visited = set()
    sizes = {}
    perimeters = {}
    plot_count = 0
    for pos, plant in garden.items():
        if pos not in visited:
            result = fill_plot(pos, garden, plant, plot_count, visited)
            sizes[plot_count] = result[0]
            perimeters[plot_count] = result[1]
            plot_count += 1

    sides = compute_sides(garden)

    part_1 = 0
    part_2 = 0

    for plot_id in range(plot_count):
        part_1 += sizes[plot_id] * perimeters[plot_id]
        part_2 += sizes[plot_id] * sides[plot_id]

    print("Part 1:", part_1)
    print("Part 2:", part_2)


if __name__ == "__main__":
    main()
