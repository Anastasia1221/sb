from dataclasses import dataclass
from typing import Set, List, Dict
from enum import Enum

from utils import Vec2, Orientation


@dataclass(frozen=True)
class Ship:
    coords: Set[Vec2]

    @staticmethod
    def make(length: int, head: Vec2, orientation: Orientation) -> 'Ship':
        if orientation == Orientation.Horizontal:
            return Ship({Vec2(head.x + i, head.y) for i in range(length)})
        else:
            return Ship({Vec2(head.x, head.y + i) for i in range(length)})


class CellState(Enum):
    Empty = 1  # empty cell
    Ship = 2  # ship is located here
    Hit = 3  # ship is hit but not yet dead
    Miss = 4  # cell was shot but was empty
    Dead = 5  # dead ship cell

    @staticmethod
    def is_ship_like(s: 'CellState') -> bool:
        return s in (CellState.Ship, CellState.Hit, CellState.Dead)


class GameException(Exception):
    pass


@dataclass(frozen=True)
class PlacementException(GameException):
    coord_errors: Dict[Vec2, str]


@dataclass(frozen=True)
class GenerationException(GameException):
    attempts: int


@dataclass(frozen=True)
class InvalidShotException(Exception):
    coord: Vec2
    cell_state: CellState


@dataclass(frozen=True)
class Board:
    cells: List[List[CellState]]
    ships: List[Ship]

    @property
    def size(self) -> Vec2:
        return Vec2(len(self.cells[0]), len(self.cells))

    def contains(self, coord: Vec2) -> bool:
        return 0 <= coord.x < self.size.x and 0 <= coord.y < self.size.y

    def state(self, coord: Vec2) -> CellState:
        return self.cells[coord.y][coord.x]

    def has_ship_nearby(self, coord: Vec2) -> bool:
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                c = Vec2(coord.x + x, coord.y + y)
                if c != coord and self.contains(c) and CellState.is_ship_like(self.state(c)):
                    return True

        return False

    def add_ship(self, ship: Ship):
        errs = {}
        for c in ship.coords:
            if not self.contains(c):
                err = 'out of bounds'
            elif not self.state(c) == CellState.Empty:
                err = 'non-empty'
            elif self.has_ship_nearby(c):
                err = 'touching another ship'
            else:
                err = None

            if err:
                errs[c] = err

        if errs:
            raise PlacementException(errs)

        for coord in ship.coords:
            self.cells[coord.y][coord.x] = CellState.Ship

        self.ships.append(ship)

    @property
    def is_finished(self) -> bool:
        for row in self.cells:
            for cell in row:
                if cell == CellState.Ship:
                    return False

        return True

    def shoot(self, coord: Vec2):
        state = self.state(coord)
        if state not in [CellState.Empty, CellState.Ship]:
            raise InvalidShotException(coord, state)

        new_state = {
            CellState.Empty: CellState.Miss,
            CellState.Ship: CellState.Hit
        }[state]

        self.cells[coord.y][coord.x] = new_state

        if new_state == CellState.Hit:
            for ship in self.ships:
                if all(self.state(c) == CellState.Hit for c in ship.coords):
                    for c in ship.coords:
                        self.cells[c.y][c.x] = CellState.Dead

    @staticmethod
    def make(size: Vec2) -> 'Board':
        return Board([[CellState.Empty] * size.x for _ in range(size.y)], [])
