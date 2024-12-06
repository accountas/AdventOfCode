from typing import Any


class Point:
    def __init__(self, *values):
        self.values = values

        for name, idx in [("i", 0), ("j", 1), ("k", 2), ("x", 0), ("y", 1), ("z", 2)]:
            if idx < len(values):
                setattr(self, name, values[idx])

    def __repr__(self):
        return f"Point({', '.join(map(str, self.values))})"

    def __eq__(self, other):
        return self.values == other.values

    def __add__(self, other):
        return Point(*(a + b for a, b in zip(self.values, other.values)))

    def __sub__(self, other):
        return Point(*(a - b for a, b in zip(self.values, other.values)))

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(*(a * b for a, b in zip(self.values, other.values)))
        return Point(*(a * other for a in self.values))

    def __getitem__(self, idx):
        return self.values[idx]

    def __setitem__(self, idx, value):
        self.values[idx] = value

    def __hash__(self) -> int:
        return hash(tuple(self.values))