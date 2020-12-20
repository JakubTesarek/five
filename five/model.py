import numpy
from enum import Enum

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f'<{self.x}:{self.y}>'

    def _get_adjacent(self, delta_x, delta_y):
        try:
            return Coordinate(self.x + delta_x, self.y + delta_y)
        except ValueError:
            return None

    @property
    def top_righ(self):
        return self._get_adjacent(-1, -1)

    @property
    def righ(self):
        return self._get_adjacent(-1, 0)

    @property
    def bottom_righ(self):
        return self._get_adjacent(-1, 1)

    @property
    def bottom(self):
        return self._get_adjacent(-1, 1)

    @property
    def bottom_left(self):
        return self._get_adjacent(1, 1)

    @property
    def left(self):
        return self._get_adjacent(1, 0)

    @property
    def top_left(self):
        return self._get_adjacent(1, -1)

    @property
    def top(self):
        return self._get_adjacent(0, -1)
    

class Player(Enum):
    x = '˟'
    o = 'o'

    def __str__(self):
        return self.value


class Board:
    min_x, max_x = -28, 28
    min_y, max_y = -20, 20

    def __init__(self):
        self.fields = numpy.full((self.height, self.width), None)

    def __str__(self):
        result = ''
        for row in self.fields:
            for field in row:
                result += '·' if field is None else str(field)
            result += '\n'
        return result

    @property
    def width(self):
        return abs(self.min_x - self.max_x)
    
    @property
    def height(self):
        return abs(self.min_y - self.max_y)

    def _normalize_coord(self, coord):
        return coord.x - self.min_x, coord.y - self.min_y

    def _denormalize_coord(self, coord):
        return coord.x + self.min_x, coord.y + self.min_y

    def __getitem__(self, coord):
        denormalized = self._normalize_coord(coord)
        return self.fields[normalized[1], normalized[0]]

    def __setitem__(self, coord, value):
        normalized = self._normalize_coord(coord)
        self.fields[normalized[1], normalized[0]] = value