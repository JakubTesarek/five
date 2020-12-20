from __future__ import annotations
import numpy
from enum import Enum
from five_in_row import types as t


class Coord:
    """Game board coordinates."""
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        """Hash of coordinates."""
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        """String representation of coordinates."""
        return f'<{self.x}:{self.y}>'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Coord) and self.x == other.x and self.y == other.y

    def _get_adjacent(self, delta_x: int, delta_y: int) -> Coord:
        return Coord(self.x + delta_x, self.y + delta_y)

    @property
    def up_right(self) -> Coord:
        """Coordinate of point diagonally up and right."""
        return self._get_adjacent(1, -1)

    @property
    def right(self) -> Coord:
        """Coordinate of point to the right."""
        return self._get_adjacent(1, 0)

    @property
    def down_right(self) -> Coord:
        """Coordinate of point down and right."""
        return self._get_adjacent(1, 1)

    @property
    def down(self) -> Coord:
        """Coordinate of point down."""
        return self._get_adjacent(0, 1)

    @property
    def down_left(self) -> Coord:
        """Coordinate of point down and left."""
        return self._get_adjacent(-1, 1)

    @property
    def left(self) -> Coord:
        """Coordinate of point left."""
        return self._get_adjacent(-1, 0)

    @property
    def up_left(self) -> Coord:
        """Coordinate of point up and left."""
        return self._get_adjacent(-1, -1)

    @property
    def up(self) -> Coord:
        """Coordinate of point up."""
        return self._get_adjacent(0, -1)


class Player(Enum):
    """Player symbol."""
    x = '˟'
    o = 'o'

    def __str__(self) -> str:
        """String representation of symbol."""
        return self.value


class Board:
    """Playing board."""
    def __init__(self, x_bounds: t.Tuple[int], y_bounds: t.Tuple[int]) -> None:
        self.min_x, self.max_x = x_bounds
        self.min_y, self.max_y = y_bounds
        self.fields = numpy.full((self.height, self.width), None)

    def __str__(self) -> str:
        """String representation of playing board."""
        result = ''
        for row in self.fields:
            for field in row:
                result += '·' if field is None else str(field)
            result += '\n'
        return result

    @property
    def width(self) -> int:
        """Number of fields horizontally (X-dimension)."""
        return abs(self.min_x - self.max_x) + 1

    @property
    def height(self) -> int:
        """Number of fields vertically (Y-dimension)."""
        return abs(self.min_y - self.max_y) + 1

    def _normalize_coord(self, coord: Coord) -> t.Tuple[int]:
        """Map coordinate to <0;with> range."""
        return coord.x - self.min_x, coord.y - self.min_y

    def _denormalize_coord(self, coord: Coord) -> t.Tuple[int]:
        """Map coordinate to <min;max> range."""
        return coord.x + self.min_x, coord.y + self.min_y

    def __getitem__(self, coord: Coord) -> t.Optional[Player]:
        """Get field value."""
        denormalized = self._denormalize_coord(coord)
        return self.fields[denormalized[1], denormalized[0]]

    def __setitem__(self, coord: Coord, value: Player) -> None:
        """Set field value."""
        normalized = self._normalize_coord(coord)
        self.fields[normalized[1], normalized[0]] = value
