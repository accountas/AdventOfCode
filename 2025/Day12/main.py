from common.data import *
from common.utils import time_it
from functools import cache

from dataclasses import dataclass


@dataclass
class Region:
    width: int
    height: int
    targets: list[int]

    def area(self):
        return self.width * self.height


def parse_input(data):
    chunks = data.split("\n\n")

    presents = []
    for chunk in chunks[:-1]:
        lines = chunk.splitlines()
        presents.append(lines[1:])

    regions = []
    for line in chunks[-1].splitlines():
        size, targets = line.split(": ")
        region = Region(
            width=int(size.split("x")[0]),
            height=int(size.split("x")[1]),
            targets=list(map(int, targets.split())),
        )
        regions.append(region)

    return presents, regions


def main():
    data = get_data(year=2025, day=12, sample=False)
    presents, regions = parse_input(data)

    present_sizes = ["".join(p).count("#") for p in presents]

    can_fit = 0
    for region in regions:
        if (region.width // 3) * (region.height // 3) >= sum(region.targets):
            can_fit += 1
        elif region.area() < sum(t * p for t, p in zip(region.targets, present_sizes)):
            pass
        else:
            raise NotImplemented("Better luck next time")

    print("Answer:", can_fit)


if __name__ == "__main__":
    time_it(main)
