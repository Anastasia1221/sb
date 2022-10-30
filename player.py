from abc import ABC, abstractmethod
import random

from models import Board, Ship, PlacementException, InvalidShotException
from utils import Vec2, Orientation


class Player(ABC):
    def __init__(self, name: str):
        self.name = name

    def on_before_placement(self, board: Board):
        pass

    @abstractmethod
    def gen_ship(self, length: int) -> Ship:
        pass

    def on_invalid_placement(self, err: PlacementException):
        pass

    @abstractmethod
    def fire(self) -> Vec2:
        pass

    def on_invalid_shot(self, err: InvalidShotException):
        pass


class AiPlayer(Player):
    def __init__(self, name: str, board_size: Vec2):
        super().__init__(name)
        self._board_size = board_size

        self._shots = [Vec2(x, y) for x in range(board_size.x) for y in range(board_size.y)]
        random.shuffle(self._shots)

    def gen_ship(self, length: int):
        return Ship.make(length, Vec2.make_random(Vec2.zero(), self._board_size), Orientation.make_random())

    def fire(self) -> Vec2:
        return self._shots.pop()


class HumanPlayer(Player):
    def on_before_placement(self, board: Board):
        Renderer(show_ships=True, show_contours=True).render_board(board)

    def gen_ship(self, length: int) -> Ship:
        print(f"Place ship of length {length}")
        print(f"Input format: <orientation (h or v)> <head.x> <head.y>")
        while True:
            try:
                pieces = input("Your ship: ").split()
                orient = {
                    'v': Orientation.Vertical,
                    'h': Orientation.Horizontal
                }[pieces[0]]
                x, y = [int(p) for p in pieces[1:]]
                return Ship.make(length, Vec2(x, y), orient)
            except LookupError:
                print("Please you the right format")
            except ValueError:
                print("Please you the right format")

    def on_invalid_placement(self, err: PlacementException):
        print(f"Can't place. The ship overlaps or is out of bounds. Errors: {err.coord_errors}")

    def fire(self) -> Vec2:
        print(f"Make your shot")
        print(f"Input format: <x> <y>")

        while True:
            try:
                text = input("Your shot: ")
                x, y = [int(p) for p in text.split()]
                return Vec2(x, y)
            except ValueError:
                print("Please you the right format")

    def on_invalid_shot(self, err: InvalidShotException):
        print(f"Can't fire at {err.coord}")
