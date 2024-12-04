class Point:
    def __init__(self, *values):
        self.values = values
        self._index_alias = {"i": 0, "j": 1, "k": 2, "x": 0, "y": 1, "z": 2}
        self._create_attributes()

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
