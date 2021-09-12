from enum import Enum

from pygame import Color


class Vision(Enum):
    BODY = -1
    WALL = 0
    FOOD = 1

    def get_color(self):
        color = Color(100, 100, 100, 10)
        if self == Vision.FOOD:
            color = Color(0, 100, 0, 10)
        elif self == Vision.BODY:
            color = Color(250, 218, 94, 10)

        return color


class Direction(Enum):
    LEFT = (-10, 0)
    RIGHT = (10, 0)
    UP = (0, -10)
    DOWN = (0, 10)
