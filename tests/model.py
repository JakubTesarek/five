import pytest
from five_in_row.model import Coord, Player, Board, Direction


@pytest.mark.unit
class TestCoord:
    def test_hashes_equal(self):
        c1 = Coord(1, 2)
        c2 = Coord(1, 2)
        assert hash(c1) == hash(c2)

    def test_coords_equal(self):
        c1 = Coord(1, 2)
        c2 = Coord(1, 2)
        assert c1 == c2

    def test_representation(self):
        c1 = Coord(1, 2)
        assert c1.__repr__() == '<1:2>'

    @pytest.mark.parametrize('direction, result', [
        (Direction.up_right, (11, 19)),
        (Direction.right, (11, 20)),
        (Direction.down_right, (11, 21)),
        (Direction.down, (10, 21)),
        (Direction.down_left, (9, 21)),
        (Direction.left, (9, 20)),
        (Direction.up_left, (9, 19)),
        (Direction.up, (10, 19))
    ])
    def test_adjacent(self, direction, result):
        c1 = Coord(10, 20)
        c2 = c1.adjacent(direction)
        assert c2 == Coord(*result)


@pytest.mark.unit
class TestDirection:
    @pytest.mark.parametrize('direction, x, y', [
        (Direction.up_right, 1, -1),
        (Direction.right, 1, 0),
        (Direction.down_right, 1, 1),
        (Direction.down, 0, 1),
        (Direction.down_left, -1, 1),
        (Direction.left, -1, 0),
        (Direction.up_left, -1, -1),
        (Direction.up, 0, -1)
    ])
    def test_get_x_y(self, direction, x, y):
        assert direction.x == x
        assert direction.y == y

    @pytest.mark.parametrize('direction, reversed_direction', [
        (Direction.up_right, Direction.down_left),
        (Direction.right, Direction.left),
        (Direction.down_right, Direction.up_left),
        (Direction.down, Direction.up),
        (Direction.down_left, Direction.up_right),
        (Direction.left, Direction.right),
        (Direction.up_left, Direction.down_right),
        (Direction.up, Direction.down)
    ])
    def test_get_reversed_direction(self, direction, reversed_direction):
        assert direction.reversed is reversed_direction

    def test_positive_directions(self):
        for direction in Direction.positive_directions():
            assert direction in (Direction.right, Direction.down_right, Direction.down, Direction.up_right)

    def test_negative_directions(self):
        for direction in Direction.negative_directions():
            assert direction in (Direction.left, Direction.up_left, Direction.up, Direction.down_left)


@pytest.mark.unit
class TestPlayer:
    def test_has_single_instance(self):
        assert Player.x is Player.x
        assert Player.o is Player.o

    def test_players_are_not_equal(self):
        assert Player.x != Player.o

    def test_opponent(self):
        assert Player.x.opponent is Player.o
        assert Player.o.opponent is Player.x


@pytest.mark.unit
class TestBoard:
    def test_empty_board_defaults_none(self):
        board = Board((0, 3), (0, 5))
        for x in range(0, 4):
            for y in range(0, 6):
                assert board[Coord(x, y)] is None

    def test_empty_board_string_repr(self):
        board = Board((0, 4), (0, 2))
        assert str(board) == (
            '·····\n'
            '·····\n'
            '·····\n'
        )

    def test_nonempty_board_string_repr(self):
        board = Board((0, 4), (0, 2))
        board[Coord(2, 2)] = Player.x
        board[Coord(3, 0)] = Player.o
        assert str(board) == (
            '···o·\n'
            '·····\n'
            '··˟··\n'
        )

    def test_height_width(self):
        board = Board((-3, 4), (-1, 2))
        assert board.width == 8
        assert board.height == 4

    def test_get_set_item(self):
        board = Board((0, 4), (0, 2))
        board[Coord(2, 2)] = Player.x
        assert board[Coord(2, 2)] is Player.x

    @pytest.mark.parametrize('coord', [
        Coord(-1, -1),
        Coord(-1, 1),
        Coord(1, 3),
        Coord(5, 3),
    ])
    def test_set_item_out_of_bounds(self, coord):
        board = Board((0, 4), (0, 2))
        with pytest.raises(IndexError):
            board[coord] = Player.x

    @pytest.mark.parametrize('coord', [
        Coord(-1, -1),
        Coord(-1, 1),
        Coord(1, 3),
        Coord(5, 3),
    ])
    def test_get_item_out_of_bounds(self, coord):
        board = Board((0, 4), (0, 2))
        with pytest.raises(IndexError):
            board[coord]

    @pytest.mark.parametrize('coord', [
        Coord(-1, -1),
        Coord(-1, 1),
        Coord(1, 3),
        Coord(5, 3),
    ])
    def test_doesnt_contain_item_out_of_bounds(self, coord):
        board = Board((0, 4), (0, 2))
        assert coord not in board

    @pytest.mark.parametrize('coord', [
        Coord(0, 0),
        Coord(0, 1),
        Coord(0, 2),
        Coord(1, 0),
        Coord(1, 1),
        Coord(1, 2),
        Coord(2, 0),
        Coord(2, 1),
        Coord(2, 2),
    ])
    def test_contains_items_in_bounds(self, coord):
        board = Board((0, 2), (0, 2))
        assert coord in board

    def test_iterate_all_fields(self):
        board = Board((0, 1), (0, 1))
        board[Coord(0, 0)] = Player.x
        board[Coord(1, 1)] = Player.o

        assert list(board.fields()) == [
            (Coord(0, 0), Player.x),
            (Coord(1, 0), None),
            (Coord(0, 1), None),
            (Coord(1, 1), Player.o)
        ]

    def test_iterate_occupied_fields(self):
        board = Board((0, 1), (0, 1))
        board[Coord(0, 0)] = Player.x
        board[Coord(1, 1)] = Player.o

        assert list(board.occupied_fields()) == [
            (Coord(0, 0), Player.x),
            (Coord(1, 1), Player.o)
        ]

    def test_iterate_fields_occupied_by_player(self):
        board = Board((0, 1), (0, 1))
        board[Coord(0, 0)] = Player.x
        board[Coord(0, 1)] = Player.o
        board[Coord(1, 1)] = Player.x

        assert list(board.occupied_fields(Player.x)) == [
            (Coord(0, 0), Player.x),
            (Coord(1, 1), Player.x)
        ]

    def test_iterate_open_fields(self):
        board = Board((0, 1), (0, 1))
        board[Coord(0, 1)] = Player.o

        assert list(board.open_fields()) == [
            Coord(0, 0),
            Coord(1, 0),
            Coord(1, 1)
        ]

    def test_open_field(self):
        board = Board((0, 1), (0, 1))
        assert board.is_open(Coord(0, 0))

    def test_not_open_field(self):
        board = Board((0, 1), (0, 1))
        board[Coord(0, 0)] = Player.o
        assert not board.is_open(Coord(0, 0))
