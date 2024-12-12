from common.data import *
from common.grid import *
from common.point import *
from collections import defaultdict
from copy import copy

def compute_sides(plot):
    dirs = [
        (RIGHT, DOWN, UP),
        (RIGHT, DOWN, DOWN),
        (DOWN, RIGHT, LEFT),
        (DOWN, RIGHT, RIGHT)
    ]

    pers = defaultdict(lambda:0)
    for dir_a, dir_b, dir_c in dirs:
        pos = Point(0, 0)
        end = Point(plot.n - 1, plot.m - 1)
        while plot.is_valid(pos):
            plant_last = plot[pos]
            is_side_last = plot[pos] != plot[pos + dir_c]
            pos_start = pos
            while plot.is_valid(pos):
                pos += dir_a
                plant_now = plot[pos]
                is_side_now = plot[pos] != plot[pos + dir_c]

                if is_side_last and (plant_last != plant_now or not is_side_now):
                    pers[plant_last] += 1
                plant_last = plant_now
                is_side_last = is_side_now
            pos = pos_start + dir_b
    return pers


def main():
    input = get_data(year=2024, day=12, sample=False)
    plot = Grid.from_string(input)

    visited = set()

    def dfs(pos, plant, plot_idx):
        if pos in visited:
            return 0, 0
        visited.add(pos)
        plot[pos] = plot_idx

        area = 1
        per = 4 - len(list(plot.neighbours(pos)))

        for neigh in plot.neighbours(pos):
            if plot[neigh] == plant:
                a, b = dfs(neigh, plant, plot_idx)
                area += a
                per += b
            else:
                per += 1
        return area, per
    
    plot_size = {}
    plot_per = {}
    num_plots = 0
    for pos, plant in plot.items():
        if pos not in visited:
            a, b = dfs(pos, plant, num_plots)
            plot_size[num_plots] = a
            plot_per[num_plots] = b
            num_plots += 1

    plot_sides = compute_sides(plot)


    part_1 = 0
    part_2 = 0

    for plot in range(num_plots):
        part_1 += plot_size[plot] * plot_per[plot]
        part_2 += plot_sides[plot] * plot_size[plot]
    

    print(part_1)
    print(part_2)




if __name__ == "__main__":
    main()
