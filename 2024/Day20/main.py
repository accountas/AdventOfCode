from common.data import *
from common.point import *
from common.grid import *

from tqdm import tqdm
from collections import defaultdict, deque
from time import time


def bfs(grid, start, wall="#"):
    queue = deque([start])
    dist = {start: 0}

    while queue:
        current = queue.popleft()
        for neighbor in grid.neighbours(current):
            if neighbor not in dist and grid[neighbor] != wall:
                dist[neighbor] = dist[current] + 1
                queue.append(neighbor)

    return dist


def find_cheats(grid, end, max_cheat):
    best_cheats = defaultdict(lambda: 0)
    dist = bfs(grid, end)

    deltas = [
        (Point(i, j), abs(i) + abs(j))
        for i in range(-max_cheat, max_cheat + 1)
        for j in range(-max_cheat, max_cheat + 1)
        if abs(i) + abs(j) <= max_cheat
    ]

    for enter in tqdm(grid.find("."), f"Finding cheats of length {max_cheat}"):
        for delta, cheat_length in deltas:
            exit = enter + delta

            dist_enter = dist.get(enter)
            dist_exit = dist.get(exit)

            if dist_enter is None or dist_exit is None:
                continue

            save = dist_enter - dist_exit - cheat_length
            best_cheats[(enter, exit)] = max(best_cheats[(enter, exit)], save)

    return best_cheats


def main():
    input = get_data(year=2024, day=20, sample=False)
    grid = Grid.from_string(input)

    start = grid.find("S")[0]
    end = grid.find("E")[0]
    grid[start] = "."
    grid[end] = "."

    part_1 = sum(save >= 100 for save in find_cheats(grid, end, 2).values())
    part_2 = sum(save >= 100 for save in find_cheats(grid, end, 20).values())

    print("Part 1:", part_1)
    print("Part 2:", part_2)


if __name__ == "__main__":
    start = time()
    main()
    print(f"Time: {time()-start:.4f} sec")
