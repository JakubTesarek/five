import pytest
from five.model import Coord, Player, Board
from textwrap import dedent


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

    def test_up_right(self):
        c1 = Coord(1, 2)
        c2 = c1.up_right
        assert c2.x == 2
        assert c2.y == 1

    def test_righ(self):
        c1 = Coord(1, 2)
        c2 = c1.right
        assert c2.x == 2
        assert c2.y == 2

    def test_down_righ(self):
        c1 = Coord(1, 2)
        c2 = c1.down_right
        assert c2.x == 2
        assert c2.y == 3

    def test_down(self):
        c1 = Coord(1, 2)
        c2 = c1.down
        assert c2.x == 1
        assert c2.y == 3

    def test_down_left(self):
        c1 = Coord(1, 2)
        c2 = c1.down_left
        assert c2.x == 0
        assert c2.y == 3

    def test_left(self):
        c1 = Coord(1, 2)
        c2 = c1.left
        assert c2.x == 0
        assert c2.y == 2

    def test_up_left(self):
        c1 = Coord(1, 2)
        c2 = c1.up_left
        assert c2.x == 0
        assert c2.y == 1

    def test_up(self):
        c1 = Coord(1, 2)
        c2 = c1.up
        assert c2.x == 1
        assert c2.y == 1


@pytest.mark.unit
class TestPlayer:
    def test_has_single_instance(self):
        assert Player.x is Player.x
        assert Player.o is Player.o

    def test_players_are_not_equal(self):
        assert Player.x != Player.o


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