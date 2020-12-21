import pytest
from five_in_row.model import Player, Coord, Board, Direction
from five_in_row.analysis import Sequence, Analysis
from random import shuffle


@pytest.mark.unit
class TestSequence:
    def test_attributes(self):
        s = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0)])
        assert s.player is Player.x
        assert s.direction is Direction.right
        assert s.fields == [Coord(0, 0), Coord(1, 0)]

    def test_sequence_length(self):
        s = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0)])
        assert len(s) == 2

    def test_sequence_to_string(self):
        s = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0)])
        assert str(s) == '(Direction.right: <0:0>,<1:0>)'

    def test_sequence_repre(self):
        s = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0)])
        assert s.__repr__() == '(Direction.right: <0:0>,<1:0>)'

    def test_sum_sequences(self):
        s1 = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0)])
        s2 = Sequence(Player.x, Direction.right, [Coord(2, 0), Coord(3, 0)])
        s3 = s1 + s2
        assert s3.fields == [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(3, 0)]
        assert s3.player is Player.x
        assert s3.direction is Direction.right

    def test_sequence_equal(self):
        s1 = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0)])
        s2 = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0)])
        assert s1 == s2

    def test_sequence_not_equal_with_different_player(self):
        s1 = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0)])
        s2 = Sequence(Player.o, Direction.right, [Coord(0, 0), Coord(1, 0)])
        assert s1 != s2

    def test_sequence_not_equal_with_different_coordinates(self):
        s1 = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0)])
        s2 = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(0, 1)])
        assert s1 != s2

    def test_sequence_not_equal_with_different_direction(self):
        s1 = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0)])
        s2 = Sequence(Player.x, Direction.left, [Coord(0, 0), Coord(1, 0)])
        assert s1 != s2


@pytest.mark.unit
class TestAnalysis:
    def test_sequence_detection(self):
        b = Board((0, 20), (0, 10))
        b[Coord(10, 5)] = Player.x
        b[Coord(11, 5)] = Player.x
        b[Coord(12, 5)] = Player.x
        b[Coord(13, 5)] = Player.x
        b[Coord(14, 5)] = Player.x
        b[Coord(11, 6)] = Player.x
        a = Analysis(b)

        assert a.find_sequences(Player.x) == [
            Sequence(Player.x, Direction.right, [Coord(10, 5), Coord(11, 5), Coord(12, 5), Coord(13, 5), Coord(14, 5)]),
            Sequence(Player.x, Direction.right, [Coord(11, 6)]),
            Sequence(Player.x, Direction.down_right, [Coord(10, 5), Coord(11, 6)]),
            Sequence(Player.x, Direction.down_right, [Coord(11, 5)]),
            Sequence(Player.x, Direction.down_right, [Coord(12, 5)]),
            Sequence(Player.x, Direction.down_right, [Coord(13, 5)]),
            Sequence(Player.x, Direction.down_right, [Coord(14, 5)]),
            Sequence(Player.x, Direction.down, [Coord(10, 5)]),
            Sequence(Player.x, Direction.down, [Coord(11, 5), Coord(11, 6)]),
            Sequence(Player.x, Direction.down, [Coord(12, 5)]),
            Sequence(Player.x, Direction.down, [Coord(13, 5)]),
            Sequence(Player.x, Direction.down, [Coord(14, 5)]),
            Sequence(Player.x, Direction.up_right, [Coord(10, 5)]),
            Sequence(Player.x, Direction.up_right, [Coord(11, 5)]),
            Sequence(Player.x, Direction.up_right, [Coord(12, 5)]),
            Sequence(Player.x, Direction.up_right, [Coord(13, 5)]),
            Sequence(Player.x, Direction.up_right, [Coord(14, 5)]),
            Sequence(Player.x, Direction.up_right, [Coord(11, 6), Coord(12, 5)])
        ]

    def test_sequence_detection_on_edge(self):
        b = Board((0, 1), (0, 1))
        b[Coord(1, 1)] = Player.x
        a = Analysis(b)

        assert a.find_sequences(Player.x) == [
            Sequence(Player.x, Direction.right, [Coord(1, 1)]),
            Sequence(Player.x, Direction.down_right, [Coord(1, 1)]),
            Sequence(Player.x, Direction.down, [Coord(1, 1)]),
            Sequence(Player.x, Direction.up_right, [Coord(1, 1)])
        ]

    def test_sequence_detection_surrounded_by_oponnent(self):
        b = Board((0, 1), (0, 1))
        b[Coord(0, 0)] = Player.x
        b[Coord(0, 1)] = Player.o
        b[Coord(1, 0)] = Player.o
        b[Coord(1, 1)] = Player.o
        a = Analysis(b)

        assert a.find_sequences(Player.x) == [
            Sequence(Player.x, Direction.right, [Coord(0, 0)]),
            Sequence(Player.x, Direction.down_right, [Coord(0, 0)]),
            Sequence(Player.x, Direction.down, [Coord(0, 0)]),
            Sequence(Player.x, Direction.up_right, [Coord(0, 0)])
        ]


@pytest.mark.performance
class TestAnalysisPerformance:
    def test_50x50_analisys(self, benchmark):
        b = Board((0, 49), (0, 49))
        fields = list(b.open_fields())
        shuffle(fields)
        for i, coord in enumerate(fields):  # fill board with random plays
            b[coord] = Player.x if i % 2 else Player.o

        a = Analysis(b)

        benchmark(a.find_sequences, Player.x)