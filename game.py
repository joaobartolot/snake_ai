from pygame import font
from food import Food
from pygame.constants import KEYDOWN
from pygame.time import Clock
from snake import Snake
from constants import *
import pygame
from pygame import Surface, draw


pygame.init()
pygame.display.set_caption("Snake Game")
screen: Surface = pygame.display.set_mode((WIDTH, HEIGH))

text_font = font.SysFont("arial", 16)


def show_gameover(screen: Surface):
    text = text_font.render(
        "You died", True, WHITE)
    screen.blit(text, [(WIDTH/2)-(text.get_size()[0]/2),
                (HEIGH/2)-(text.get_size()[1]/2)])

    text = text_font.render(
        "press 'Q' to quit the game and 'F' play again", True, WHITE)
    screen.blit(text, [(WIDTH/2)-(text.get_size()[0]/2),
                (HEIGH/2)+(text.get_size()[1])])


def show_score(screen: Surface, score: int):
    text = text_font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, [0, 0])


def main():
    snake = Snake()
    food = Food()

    clock = Clock()

    running = True
    gameover = False

    while running:
        screen.fill(BLACK)

        while gameover == True:
            screen.fill(BLACK)
            show_score(screen, snake.score)
            show_gameover(screen)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False
                        gameover = False
                    if event.key == pygame.K_f:
                        main()

            pygame.display.update()
        if running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == KEYDOWN:
                    snake.change_direction(event.key)

            show_score(screen, snake.score)

            snake.update(screen)
            food.draw(screen)

            if snake.pos() == food.pos():
                snake.eat()
                food = Food()

        gameover = snake.is_dead()

        clock.tick(15)

        pygame.display.update()


if __name__ == "__main__":
    main()
