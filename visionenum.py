from enum import Enum


class Vision(Enum):
    BODY = -1
    NOTHING = 0
    FOOD = 1


class Direction(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'
