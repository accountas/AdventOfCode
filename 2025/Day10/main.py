from common.data import *
from common.utils import time_it
import functools as ft
from collections import deque
import z3


def parse_input(data):
    to_list = lambda s: list(map(int, s[1:-1].split(",")))
    problems = []
    for line in data.splitlines():
        tokens = line.split()
        target = tokens[0][1:-1]
        weights = to_list(tokens[-1])
        buttons = [to_list(b) for b in tokens[1:-1]]
        problems.append((target, buttons, weights))
    return problems


def part_1(target, buttons):
    def press(lights, button):
        new_state = list(lights)
        for idx in button:
            new_state[idx] = "." if new_state[idx] == "#" else "#"
        return "".join(new_state)

    bfs_queue = deque()
    start = "." * len(target)
    distances = {start: 0}
    bfs_queue.append(start)

    while len(bfs_queue) > 0:
        node = bfs_queue.popleft()
        if node == target:
            break
        for button in buttons:
            new_node = press(node, button)
            if new_node not in distances:
                distances[new_node] = distances[node] + 1
                bfs_queue.append(new_node)

    return distances[target]


def part_2(target, buttons):
    solver = z3.Optimize()

    button_vars = []
    for button in range(len(buttons)):
        var = z3.Int(f"button_{button}")
        solver.add(var >= 0)
        button_vars.append(var)

    for target_idx, value in enumerate(target):
        matching_vars = []
        for button_idx, button in enumerate(buttons):
            if target_idx in button:
                matching_vars.append(button_vars[button_idx])
        total = ft.reduce(lambda a, b: a + b, matching_vars)
        solver.add(total == value)

    total_presses = ft.reduce(lambda a, b: a + b, button_vars)
    solver.minimize(total_presses)

    if solver.check() == z3.sat:
        model = solver.model()
        return model.evaluate(total_presses).as_long()
    else:
        raise RuntimeError("Something went wrong, unsatisfiable")


def main():
    data = get_data(year=2025, day=10, sample=False)
    problems = parse_input(data)

    part_1_total = 0
    part_2_total = 0
    for target, buttons, weights in problems:
        part_1_total += part_1(target, buttons)
        part_2_total += part_2(weights, buttons)

    print("Part 1:", part_1_total)
    print("Part 2:", part_2_total)


if __name__ == "__main__":
    time_it(main)
