from visionenum import Direction
from food import Food
from pygame.constants import HAT_CENTERED
from constants import GREEN, HEIGH, RED, WHITE, WIDTH
from pygame import Surface, draw
from pygame import K_LEFT, K_RIGHT, K_UP, K_DOWN


class Snake:
    def __init__(self):
        self.head: Head = Head()
        self.body: list[Body] = [
            Body(self.head.x - self.head.size, self.head.y),
            Body(self.head.x - (self.head.size * 2), self.head.y),
        ]
        self.score = 0

    def vision(self, food: Food):
        # TODO: implement vision for the AI
        # look_x = (
        #     (self.head.x + self.head.size) if self.vel() == (10, 0) else 0,
        #     (self.head.x - self.head.size) if self.vel() == (-10, 0) else WIDTH,
        # )
        # look_y = (
        #     (self.head.y + self.head.size) if self.vel() == (0, 10) else 0,
        #     (self.head.y - self.head.size) if self.vel() == (0, -10) else HEIGH,
        # )

        vision = [0, 0, 0, 0, 0]

        if self.head.vel() == Direction.LEFT:
            for i in range():
                pass
            # # See in the x axis
            # for x in range(look_x[0], look_x[1], 10):

    def update(self, screen):
        last_head_pos = self.head.pos()
        self.head.update(screen)

        pos = []

        for i, b in enumerate(self.body):
            if self.head.moving:
                if (i == 0):
                    pos.append(b.pos())
                    b.update(screen, last_head_pos)
                else:
                    pos.append(b.pos())
                    b.update(screen, pos[0])
                    pos.pop(0)
            else:
                b.update(screen, b.pos())

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
        for b in self.body:
            if self.head.pos() == b.pos():
                return True

        if self.head.x > WIDTH or self.head.x < 0:
            return True
        elif self.head.y > HEIGH or self.head.y < 0:
            return True

        return False

    def pos(self) -> set[int, int]:
        return self.head.x, self.head.y

    def __len__(self):
        return len(self.body) + 1


class Body:
    def __init__(self, x: int = (WIDTH/2), y: int = (HEIGH/2), c=WHITE) -> None:
        self.x: int = x
        self.y: int = y
        self.size: int = 10
        self.velocity_x: int = 0
        self.velocity_y: int = 0
        self.direction: Direction = None
        self.color = c

    def update(self, screen: Surface, next_pos: set[int, int]) -> None:
        self.__update_vel(next_pos)
        self.__update_pos(next_pos)

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

    def update(self, screen: Surface) -> None:
        self.__update_pos()

        draw.rect(screen, WHITE, [self.x,
                  self.y, self.size, self.size])

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
