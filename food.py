from pygame import draw
from constants import GREEN, HEIGH, WIDTH
import random


class Food:
    def __init__(self) -> None:
        self.size = 10
        self.x = random.randint(0, ((WIDTH-self.size)/10)) * 10
        self.y = random.randint(0, ((HEIGH-self.size)/10)) * 10

    def draw(self, screen):
        draw.rect(screen, GREEN, [self.x,
                  self.y, self.size, self.size])

    def pos(self) -> set[int, int]:
        return self.x, self.y
