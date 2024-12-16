from common.data import *
from common.point import *
from common.grid import *
from heapq import heappush, heappop


def dijkstra(grid, pos, start_dirs):
    queue = [(0, (pos, dir)) for dir in start_dirs]

    distances = {start: 0 for start in queue}
    visited = set()

    while queue:
        dist, (pos, direction) = heappop(queue)

        if (pos, direction) in visited:
            continue
        
        visited.add((pos, direction))

        for new_direction in DIRECTIONS:
            if new_direction == direction:
                child = (pos + new_direction, new_direction)
                points = 1
            else:
                child = (pos, new_direction)
                points = 1000 if new_direction != direction * -1 else 2000

            if not grid.is_valid(child[0]) or grid[child[0]] == "#":
                continue

            if child not in distances or distances[child] > dist + points:
                distances[child] = dist + points
                heappush(queue, (dist + points, child))

    return distances


def main():
    input = get_data(year=2024, day=16, sample=False)
    grid = Grid.from_string(input)

    start = grid.find("S")[0]
    end = grid.find("E")[0]

    distances_front = dijkstra(grid, start, [RIGHT])
    distances_back = dijkstra(grid, end, DIRECTIONS)

    best_score = min(distances_front[end, dir] for dir in DIRECTIONS)
    good_spots = set([start, end])

    for spot in grid.find("."):
        for direction in DIRECTIONS:
            front = (spot, direction)
            back = (spot, direction * -1)
            if distances_front[front] + distances_back[back] == best_score:
                good_spots.add(spot)

    print("Part 1:", best_score)
    print("Part 2:", len(good_spots))


if __name__ == "__main__":
    main()
