
from functools import total_ordering

@total_ordering
class Point:
    __slots__ = ("values",)

    def __init__(self, *values):
        self.values = list(values)

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
    
    def __lt__(self, other):
        return self.values < other.values

    @staticmethod
    def _make_property(index: int):
        def getter(self):
            return self.values[index]
        def setter(self, value):
            self.values[index] = value
        return property(getter, setter)

    i = _make_property(0)
    j = _make_property(1)
    k = _make_property(2)

    x = _make_property(0)
    y = _make_property(1)
    z = _make_property(2)
