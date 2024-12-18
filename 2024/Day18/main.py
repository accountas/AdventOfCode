from common.data import *
from common.point import *
from common.grid import *
from collections import deque
from tqdm import tqdm


def parse_input(input):
    return [Point(*list(map(int, line.split(",")[::-1]))) for line in input.splitlines()]


def points_in_shortest_path(grid, start, end):
    queue = deque([start])
    dist = {start: 0}
    prev = {start: None}

    while queue:
        current = queue.popleft()
        if current == end:
            break

        for neighbor in grid.neighbours(current):
            if neighbor not in dist and grid[neighbor]:
                dist[neighbor] = dist[current] + 1
                prev[neighbor] = current
                queue.append(neighbor)

    if end not in dist:
        return None

    path = set()
    node = end
    while node is not None:
        path.add(node)
        node = prev.get(node)

    return path


def main():
    input = get_data(year=2024, day=18, sample=False)
    points = parse_input(input)

    start = Point(0, 0)
    end = Point(70, 70)
    grid = Grid.empty(71, 71, True)
    fall_first = 1024

    for point in points[:fall_first]:
        grid[point] = False

    shortest_path = points_in_shortest_path(grid, start, end)

    print("Part 1", len(shortest_path) - 1)

    for point in points[fall_first:]:
        grid[point] = False
        if point in shortest_path:
            shortest_path = points_in_shortest_path(grid, start, end)
            a += 1

        if shortest_path is None:
            break

    print(
        f"Part 2: {point.j},{point.i}",
    )


if __name__ == "__main__":
    main()
