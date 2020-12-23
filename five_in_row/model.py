from __future__ import annotations
import numpy
from enum import Enum
from five_in_row import types as t
import math


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
        """Returns True if given object is Coord pointing to the same square."""
        return isinstance(other, Coord) and self.x == other.x and self.y == other.y

    def adjacent(self, direction: Direction) -> Coord:
        """Returns adjacent Coord in given direction."""
        return Coord(self.x + direction.x, self.y + direction.y)

    def distance(self, coord: Coord) -> float:
        """Calculate distance from to another Coord."""
        return math.sqrt(pow(abs(self.x - coord.x), 2) + pow(abs(self.y - coord.y), 2))


class Direction(Enum):
    """Direction on a board."""

    up_right = (1, -1)
    right = (1, 0)
    down_right = (1, 1)
    down = (0, 1)
    down_left = (-1, 1)
    left = (-1, 0)
    up_left = (-1, -1)
    up = (0, -1)

    @property
    def x(self) -> int:
        """Delta of X coordinate."""
        return self.value[0]

    @property
    def y(self) -> int:
        """Delta of Y coordinate."""
        return self.value[1]

    @property
    def reversed(self) -> Direction:
        """Direction rotated by 180deg."""
        return Direction((-self.x, -self.y))

    @classmethod
    def positive_directions(cls) -> t.List[Direction]:
        """List of directions going generally from left to right and from up to bottom."""
        return [cls.right, cls.down_right, cls.down, cls.up_right]

    @classmethod
    def negative_directions(cls) -> t.List[Direction]:
        """List of directions going generaly from right to left and from buttom up."""
        return [cls.left, cls.up_left, cls.up, cls.down_left]


class Player(Enum):
    """Player symbol."""
    x = '˟'
    o = 'o'

    def __str__(self) -> str:
        """String representation of symbol."""
        return self.value

    @property
    def opponent(self) -> Player:
        if self is Player.x:
            return Player.o
        return Player.x


class Board:
    """Playing board."""
    def __init__(self, x_bounds: t.Tuple[int, int], y_bounds: t.Tuple[int, int]) -> None:
        self.min_x, self.max_x = x_bounds
        self.min_y, self.max_y = y_bounds
        self._fields = numpy.full((self.height, self.width), None)

    def __str__(self) -> str:
        """String representation of playing board."""
        result = ''
        for row in self._fields:
            for field in row:
                result += '·' if field is None else str(field)
            result += '\n'
        return result

    def fields(self) -> t.Iterator[t.Tuple[Coord, t.Optional[Player]]]:
        """Iterate over all fields in format (Coord, Player)."""
        for y in range(self._fields.shape[0]):
            for x in range(self._fields.shape[1]):
                coord = Coord(x, y)
                yield coord, self[coord]

    def occupied_fields(self, player: Player = None) -> t.Iterator[t.Tuple[Coord, Player]]:
        """Iterate over all occupied fields in format (Coord, Player)."""
        for coord, _player in self.fields():
            if _player is not None:
                if player is None or player is _player:
                    yield coord, _player

    def open_fields(self) -> t.Iterator[Coord]:
        """Iterate over open fields"""
        for coord, player in self.fields():
            if player is None:
                yield coord

    def is_open(self, coord: Coord) -> bool:
        """Returns True if given coordinate is empty."""
        return self[coord] is None

    @property
    def width(self) -> int:
        """Number of fields horizontally (X-dimension)."""
        return abs(self.min_x - self.max_x) + 1

    @property
    def height(self) -> int:
        """Number of fields vertically (Y-dimension)."""
        return abs(self.min_y - self.max_y) + 1

    def _normalize_coord(self, coord: Coord) -> t.Tuple[int, int]:
        """Map coordinate to <0;with> range."""
        return coord.x - self.min_x, coord.y - self.min_y

    def _denormalize_coord(self, coord: Coord) -> t.Tuple[int, int]:
        """Map coordinate to <min;max> range."""
        return coord.x + self.min_x, coord.y + self.min_y

    def __getitem__(self, coord: Coord) -> t.Optional[Player]:
        """Get field value."""
        if coord not in self:
            raise IndexError(f'Coordinate {coord} is out of board bounds.')
        denormalized = self._denormalize_coord(coord)
        return self._fields[denormalized[1], denormalized[0]]

    def __setitem__(self, coord: Coord, value: Player) -> None:
        """Set field value."""
        if coord not in self:
            raise IndexError(f'Coordinate {coord} is out of board bounds.')
        normalized = self._normalize_coord(coord)
        self._fields[normalized[1], normalized[0]] = value

    def __contains__(self, coord: Coord) -> bool:
        """Returns True if giver coord is in bounds."""
        return (self.min_x <= coord.x <= self.max_x) and (self.min_y <= coord.y <= self.max_y)
