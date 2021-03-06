import numpy as np
import pygame
from visionenum import Direction, Vision
from food import Food
from pygame.constants import HAT_CENTERED
from constants import AI_PLAYING, BLACK, GREEN, GREY, HEIGH, RED, WHITE, WIDTH
from pygame import Surface, draw
from pygame import K_LEFT, K_RIGHT, K_UP, K_DOWN
import math


class Snake:
    def __init__(self, direction: Direction = None):
        self.head: Head = Head()
        self.body: list[Body] = [
            Body(self.head.x - self.head.size, self.head.y),
            Body(self.head.x - (self.head.size * 2), self.head.y),
        ]
        self.vision: dict[str, tuple[(Vision, int)]] = {}
        self.score = 0
        self.head.direction = direction
        self.best_distance_food = WIDTH
        self.lifetime = 0
        self.life_left = 200

    def look_around(self, food: Food):
        # TODO: implement vision for the AI
        self.vision['left'] = (Vision.WALL, self.head.x)
        self.vision['right'] = (Vision.WALL,  WIDTH - self.head.x)
        self.vision['up'] = (Vision.WALL, self.head.y)
        self.vision['down'] = (Vision.WALL,  HEIGH - self.head.y)

        for x in range(0, WIDTH + self.head.size, self.head.size):
            for b in self.body:
                if b.x == x and b.y == self.head.y:
                    if self.head.x > x:
                        self.vision['left'] = (Vision.BODY, self.head.x - x)
                    else:
                        self.vision['right'] = (Vision.BODY,  x - self.head.x)
                        break
            if food.x == x and food.y == self.head.y:
                if self.head.x > x:
                    self.vision['left'] = (Vision.FOOD, self.head.x - x)
                    if self.vision['left'][1] < self.best_distance_food:
                        self.best_distance_food = self.vision['left'][1]
                else:
                    if self.vision['right'][0] != Vision.BODY or self.vision['right'][1] < x-self.head.x:
                        self.vision['right'] = (Vision.FOOD,  x - self.head.x)
                        if self.vision['right'][1] < self.best_distance_food:
                            self.best_distance_food = self.vision['right'][1]
                        break

        for y in range(0, HEIGH + self.head.size, self.head.size):
            for b in self.body:
                if b.y == y and b.x == self.head.x:
                    if self.head.y > y:
                        self.vision['up'] = (Vision.BODY, self.head.y - y)
                    else:
                        self.vision['down'] = (Vision.BODY,  y - self.head.y)
                        break
            if food.y == y and food.x == self.head.x:
                if self.head.y > y:
                    self.vision['up'] = (Vision.FOOD, self.head.y - y)
                else:
                    if self.vision['down'][0] != Vision.BODY or self.vision['down'][1] > y-self.head.y:
                        self.vision['down'] = (Vision.FOOD,  y - self.head.y)
                        break

    def __draw_vision(self, screen: Surface):
        if len(self.vision.values()) > 0:
            color = pygame.Color(100, 100, 100, 10)
            for y in range(0, HEIGH + self.head.size, self.head.size):
                if y < self.head.y:
                    color = self.vision['up'][0].get_color()
                    draw.circle(screen, color, (self.head.x +
                                                (self.head.size/2), y + (self.head.size/2)), 2)
                elif y > self.head.y:
                    color = self.vision['down'][0].get_color()
                    draw.circle(screen, color, (self.head.x +
                                                (self.head.size/2), y + (self.head.size/2)), 2)

            for x in range(0, WIDTH + self.head.size, self.head.size):
                if x < self.head.x:
                    color = self.vision['left'][0].get_color()
                    draw.circle(screen, color, (x + (self.head.size/2), (self.head.y +
                                                                         (self.head.size/2))), 2)
                elif x > self.head.x:
                    color = self.vision['right'][0].get_color()
                    draw.circle(screen, color,  (x + (self.head.size/2), (self.head.y +
                                                                          (self.head.size/2))), 2)

    def get_vision_data(self) -> list[int, int, int, int]:
        return np.array([[
            self.vision['left'][0].value,
            self.vision['right'][0].value,
            self.vision['up'][0].value,
            self.vision['down'][0].value,
        ]])

    def get_fitness(self):
        return (self.score**2)*(self.lifetime ** 2)

    def update(self, screen: Surface = None, draw: bool = False, show_vision: bool = False):
        self.lifetime += 1
        self.life_left -= 1
        last_head_pos = self.head.pos()
        if screen != None and draw:
            self.head.update(screen)
        else:
            self.head.update(draw=draw)
        pos = []

        for i, b in enumerate(self.body):
            if self.head.moving:
                if (i == 0):
                    pos.append(b.pos())
                    if screen != None and draw:
                        b.update(last_head_pos, screen)
                    else:
                        b.update(last_head_pos, draw=draw)
                else:
                    pos.append(b.pos())
                    if screen != None and draw:
                        b.update(pos[0], screen)
                    else:
                        b.update(pos[0], draw=draw)
                    pos.pop(0)
            else:
                if screen != None and draw:
                    b.update(b.pos(), screen)
                else:
                    b.update(b.pos(), draw=draw)

        if show_vision:
            self.__draw_vision(screen)

    def change_direction(self, key):
        self.head.change_direction(key)

    def eat(self):
        self.score += 1

        last = self.body[-1]

        if last.vel() == (10, 0):
            self.body.append(Body(last.x - last.size, last.y))
        elif last.vel() == (0, 10):
            self.body.append(Body(last.x, last.y - last.size))
        elif last.vel() == (-10, 0):
            self.body.append(Body(last.x + last.size, last.y))
        elif last.vel() == (0, -10):
            self.body.append(Body(last.x, last.y + last.size))

    def is_dead(self):
        if AI_PLAYING and self.life_left == 0:
            return True

        for b in self.body:
            if self.head.pos() == b.pos():
                self.score += -0.25
                return True

        if self.head.x > WIDTH or self.head.x < 0:
            self.score += -0.1
            return True
        elif self.head.y > HEIGH or self.head.y == -10:
            self.score += -0.1
            return True

        return False

    def pos(self) -> set[int, int]:
        return self.head.x, self.head.y

    def __len__(self):
        return len(self.body) + 1


class Body:
    def __init__(self, x: int = (WIDTH/2), y: int = (HEIGH/2), c=WHITE) -> None:
        self.x: int = int(x)
        self.y: int = int(y)
        self.size: int = 10
        self.velocity_x: int = 0
        self.velocity_y: int = 0
        self.direction: Direction = None
        self.color = c

    def update(self, next_pos: set[int, int], screen: Surface = None, draw: bool = True) -> None:
        self.__update_vel(next_pos)
        self.__update_pos(next_pos)

        if screen != None and draw:
            self.draw(screen)

    def draw(self, screen):
        draw.rect(screen, BLACK, [
                  self.x-1, self.y-1, self.size+2, self.size+2])

        draw.rect(screen, self.color, [
                  self.x, self.y, self.size, self.size])

    def __update_vel(self, next_pos):
        if next_pos[0] != self.x:
            self.direction = Direction.RIGHT if next_pos[0] > self.x else Direction.LEFT
        elif next_pos[1] != self.y:
            self.direction = Direction.UP if next_pos[1] > self.x else Direction.DOWN

    def __update_pos(self, next_pos):
        self.x = next_pos[0]
        self.y = next_pos[1]

    def pos(self):
        return self.x, self.y

    def vel(self):
        return self.direction.value


class Head(Body):
    def __init__(self, x: int = (WIDTH/2), y: int = (HEIGH/2)) -> None:
        super().__init__(x=x, y=y)
        self.moving = False
        self.velocity: int = 10

    def update(self, screen: Surface = None, draw: bool = True) -> None:
        self.__update_pos()

        if screen != None and draw:
            self.draw(screen)

    def __update_pos(self):
        if self.direction != None:
            self.x += self.direction.value[0]
            self.y += self.direction.value[1]

    def change_direction(self, key) -> None:
        if key == K_LEFT and self.direction != Direction.RIGHT and self.moving:
            self.direction = Direction.LEFT
        elif key == K_RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT
        elif key == K_UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        elif key == K_DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN
            self.velocity_x, self.velocity_y = Direction.DOWN.value

        self.moving = True
