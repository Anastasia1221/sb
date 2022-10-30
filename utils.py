from dataclasses import dataclass
from enum import Enum
import random


@dataclass(frozen=True)
class Vec2:
    x: int
    y: int

    @staticmethod
    def zero() -> 'Vec2':
        return Vec2(0, 0)

    @staticmethod
    def make_random(start: 'Vec2', end: 'Vec2') -> 'Vec2':
        return Vec2(
            random.randrange(start.x, end.x),
            random.randrange(start.y, end.y)
        )


class Orientation(Enum):
    Vertical = "v"
    Horizontal = "h"

    @staticmethod
    def make_random() -> 'Orientation':
        return random.choice([Orientation.Horizontal, Orientation.Vertical])
