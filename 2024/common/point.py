class Point:
    def __init__(self, *values):
        self.values = values
        self._index_alias = {"i": 0, "j": 1, "k": 2, "x": 0, "y": 1, "z": 2}
        self._create_attributes()

    def is_valid_index(self, *limits):
        for value, limit in zip(self.values, limits):
            if value >= limit or value < 0:
                return False
        return True

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

    def _create_attributes(self):
        for name, idx in self._index_alias.items():

            def getter(self, _idx=idx):
                return self.values[_idx]

            def setter(self, value, _idx=idx):
                self.values[_idx] = value

            setattr(self.__class__, name, property(getter, setter))


# In matricies
UP = Point(1, 0)
DOWN = Point(-1, 0)
LEFT = Point(0, -1)
RIGHT = Point(0, 1)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

UP_LEFT = UP + LEFT
UP_RIGHT = UP + RIGHT
DOWN_LEFT = DOWN + LEFT
DOWN_RIGHT = DOWN + RIGHT
DIAGONALS = [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
ALL_DIRECTIONS = DIRECTIONS + DIAGONALS
