from __future__ import annotations
from five_in_row.model import Direction
from five_in_row import types as t

if t.TYPE_CHECKING:
    from five_in_row.model import Player, Coord, Board


class Sequence:
    required_length = 5

    """Sequence of moves of a single player."""
    def __init__(self, player: Player, direction: Direction, fields: t.List[Coord]) -> None:
        self.player = player
        self.direction = direction
        self.fields = fields
        self.start_open_points = 0
        self.end_open_points = 0

    @property
    def surrounding_open_points(self) -> int:
        return self.start_open_points + self.end_open_points

    @property
    def missing_points(self) -> int:
        return self.required_length - len(self)

    @property
    def closable(self) -> bool:
        return self.surrounding_open_points >= self.missing_points

    @property
    def closed(self) -> bool:
        return len(self) >= self.required_length

    @property
    def start(self) -> Coord:
        """First point of sequence."""
        return self.fields[0]

    @property
    def end(self) -> Coord:
        """Last point of sequence."""
        return self.fields[-1]

    def __len__(self) -> int:
        """Number of fields in sequence."""
        return len(self.fields)

    def __add__(self, sequence: Sequence) -> Sequence:
        """Sum two sequences together."""
        return Sequence(self.player, self.direction, self.fields + sequence.fields)

    def __str__(self) -> str:
        """String representation of Sequence."""
        return (
            f'({self.direction}: {",".join(str(f) for f in self.fields)}) '
            f'<{self.start_open_points}-{self.end_open_points}'
            f'{" closable" if self.closable else ""}>'
        )

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

    def _detect_open_ends(self, sequence: Sequence) -> None:
        """Count number of open squares at the ends of sequence and assign them."""
        sequence.end_open_points = self._count_open_end(
            sequence.missing_points,
            sequence.end,
            sequence.direction
        )
        sequence.start_open_points = self._count_open_end(
            sequence.missing_points,
            sequence.start,
            sequence.direction.reversed
        )

    def _count_open_end(self, missing: int, start: Coord, direction: Direction) -> int:
        """Count open squares at given end of sequence."""
        player = self.board[start]
        if not player:  # IMPOSSSIBLE
            return 0
        free_spaces = 0
        while free_spaces < missing:
            start = start.adjacent(direction)
            if start not in self.board or self.board[start] == player.opponent:
                break
            free_spaces += 1
        return free_spaces

    def find_sequences(self, player: Player) -> t.List[Sequence]:
        """Find all sequences belonging to a player."""
        sequences = []
        for direction in Direction.positive_directions():
            sequences.extend(self._find_directional_sequences(player, direction))

        for sequence in sequences:
            self._detect_open_ends(sequence)
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

        if adjacent in self.board and self.board[adjacent] == player:
            sequence += self._find_directional_sequence(adjacent, player, direction)

        return sequence

    def find_empty_adjacent_fields(self) -> t.Set[Coord]:
        """Get all empty coords that are attached to a non-empty coord."""
        fields = set()
        for field in self.board.open_fields():
            for direction in Direction:
                adjacent_field = field.adjacent(direction)
                if adjacent_field in self.board and not self.board.is_open(adjacent_field):
                    fields.add(field)
        return fields
