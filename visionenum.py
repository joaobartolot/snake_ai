from enum import Enum


class Vision(Enum):
    BODY = -1
    NOTHING = 0
    FOOD = 1


class Direction(Enum):
    LEFT = (-10, 0)
    RIGHT = (10, 0)
    UP = (0, -10)
    DOWN = (0, 10)
