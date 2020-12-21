
![Run checks](https://github.com/JakubTesarek/five/workflows/Run%20checks/badge.svg?branch=main)

# Five in a row
Five in a row is http client for [piskvorky.jobs.cz](https://piskvorky.jobs.cz/) and game state analyser.

> This library is under heavy development. Public API changes often. Features may be added or removed at any time.

## Analysing game state

To start analysing game state, you need to create a board first.

```python
from five_in_row.model import Board
board = Board((0, 10), (0, 5))
```
Board accepts 2 tuples with board bounds. (End and start point are included.) This board will start at coordinates `x:0, y: 0` (top left corner) and end at `x:10, y: 5` (bottom right corner).

Board is initialised empty. We can access individual cells with indexes:

```python
from five_in_row.model import Board, Player, Coord
board = Board((0, 10), (0, 5))

board[Coord(7, 4)] = Player.x
board[Coord(3, 5)] = Player.o
print(board)
```
Output:
```sh
···········

···········

···········

···········

·······˟···

···o·······
```

> `Board` and `Coord` provide more useful methods. See pydoc for more details.

We can then analyse our newly created board by creating new `Analysis`.

```python
from five_in_row.analysis import Analysis
analysis = Analysis(board)
```

`Analysis` provides currently single public method that returns list of all sequences of given player.

```python
analysis.find_sequences(Player.x)
```
Each sequence (`five_in_row.analysis.Sequence`) represents any number of consequent moves on a board by a player in any direction. Even isolated move is considered to be a sequence of length 1.