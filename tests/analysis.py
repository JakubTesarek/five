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
        assert str(s) == '(Direction.right: <0:0>,<1:0>) <0-0>'

    def test_sequence_with_open_ends_to_string(self):
        s = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0)])
        s.start_open_points = 3
        s.end_open_points = 5
        assert str(s) == '(Direction.right: <0:0>,<1:0>) <3-5 closable>'

    def test_sequence_repre(self):
        s = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0)])
        assert s.__repr__() == '(Direction.right: <0:0>,<1:0>) <0-0>'

    def test_sequence_repre_with_open_ends(self):
        s = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0)])
        s.start_open_points = 3
        s.end_open_points = 5
        assert s.__repr__() == '(Direction.right: <0:0>,<1:0>) <3-5 closable>'

    def test_detect_start_end_of_sequence(self):
        s = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0), Coord(2, 0)])
        assert s.start == Coord(0, 0)
        assert s.end == Coord(2, 0)

    def test_count_missing_points(self):
        s = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0), Coord(2, 0)])
        assert s.missing_points == 2

    def test_count_missing_points_complete_sequence(self):
        s = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(3, 0), Coord(4, 0)])
        assert s.missing_points == 0

    def test_count_open_points(self):
        s = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0), Coord(2, 0)])
        s.start_open_points = 3
        s.end_open_points = 5
        assert s.surrounding_open_points == 8

    def test_complete_sequence_is_closable_and_closed(self):
        s = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(3, 0), Coord(4, 0)])
        assert s.closable
        assert s.closed

    def test_incomplete_sequence_is_closable(self):
        s = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0), Coord(2, 0)])
        s.start_open_points = 3
        s.end_open_points = 5
        assert s.closable

    def test_incomplete_sequence_is_not_closable(self):
        s = Sequence(Player.x, Direction.right, [Coord(0, 0), Coord(1, 0), Coord(2, 0)])
        assert not s.closable

    def test_detect_start_end_of_sequence_of_single_point_sequence(self):
        s = Sequence(Player.x, Direction.right, [Coord(0, 0)])
        assert s.start == Coord(0, 0)
        assert s.end == Coord(0, 0)

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

    def test_sequence_opennes_detection(self):
        b = Board((0, 5), (0, 5))
        b[Coord(1, 2)] = Player.x
        b[Coord(2, 2)] = Player.x
        b[Coord(3, 2)] = Player.x
        b[Coord(4, 2)] = Player.x
        b[Coord(5, 2)] = Player.x
        b[Coord(1, 1)] = Player.o
        b[Coord(2, 1)] = Player.o
        b[Coord(3, 1)] = Player.o

        # (closable, closed, start_open_points, end_open_points) noqa: E800
        expected_values = [
            (True, True, 0, 0),
            (True, False, 1, 3),
            (False, False, 0, 3),
            (False, False, 0, 2),
            (False, False, 0, 1),
            (False, False, 2, 0),
            (False, False, 0, 3),
            (False, False, 0, 3),
            (False, False, 0, 3),
            (True, False, 2, 3),
            (True, False, 2, 3),
            (False, False, 1, 0),
            (False, False, 2, 0),
            (True, False, 3, 2),
            (True, False, 3, 1),
            (False, False, 3, 0)
        ]

        a = Analysis(b)
        for sequence in a.find_sequences(Player.x):
            expected_value = expected_values.pop(0)
            assert sequence.closable == expected_value[0]
            assert sequence.closed == expected_value[1]
            assert sequence.start_open_points == expected_value[2]
            assert sequence.end_open_points == expected_value[3]

    def test_find_empty_attached_fields(self):
        b = Board((0, 30), (0, 30))
        b[Coord(15, 15)] = Player.x
        a = Analysis(b)

        assert a.find_empty_adjacent_fields() == set([
            Coord(14, 14),
            Coord(14, 15),
            Coord(15, 14),
            Coord(16, 16),
            Coord(14, 16),
            Coord(15, 16),
            Coord(16, 15),
            Coord(16, 14)
        ])


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
