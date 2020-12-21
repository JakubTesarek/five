from __future__ import annotations
from five_in_row.model import Direction
from five_in_row import types as t

if t.TYPE_CHECKING:
    from five_in_row.model import Player, Coord, Board


class Sequence:
    """Sequence of moves of a single player."""
    def __init__(self, player: Player, direction: Direction, fields: t.List[Coord]) -> None:
        self.player = player
        self.direction = direction
        self.fields = fields

    def __len__(self) -> int:
        """Number of fields in sequence."""
        return len(self.fields)

    def __add__(self, sequence: Sequence) -> Sequence:
        """Sum two sequences together."""
        return Sequence(self.player, self.direction, self.fields + sequence.fields)

    def __str__(self) -> str:
        """String representation of Sequence."""
        return f'({self.direction}: {",".join(str(f) for f in self.fields)})'

    def __repr__(self) -> str:
        """String representation of Sequence."""
        return str(self)

    def __eq__(self, other: object) -> bool:
        """Return True if given other object is equal sequence."""
        return isinstance(other, Sequence) \
            and self.fields == other.fields \
            and self.direction is other.direction \
            and self.player is other.player


class Analysis:
    """Analysis of board state."""

    def __init__(self, board: Board) -> None:
        self.board = board

    def find_sequences(self, player: Player) -> t.List[Sequence]:
        """Find all sequences belonging to a player."""
        sequences = []
        for direction in Direction.positive_directions():
            sequences.extend(self._find_directional_sequences(player, direction))
        return sequences

    def _find_directional_sequences(self, player: Player, direction: Direction) -> t.List[Sequence]:
        """Find all sequences belonging to a player in given direction."""
        sequences = []
        solved_coords = set()
        for coord, _ in self.board.occupied_fields(player):
            if coord not in solved_coords:
                sequence = self._find_directional_sequence(coord, player, direction)
                solved_coords.update(sequence.fields)
                sequences.append(sequence)
        return sequences

    def _find_directional_sequence(self, start: Coord, player: Player, direction: Direction) -> Sequence:
        """Find sequence belonging to a player in given direction starting at given Coord."""
        sequence = Sequence(player, direction, [start])
        adjacent = start.adjacent(direction)
        try:
            if self.board[adjacent] == player:
                sequence += self._find_directional_sequence(adjacent, player, direction)
        except IndexError:
            pass
        return sequence
