import pickle
from visionenum import Direction
from numpy.core.numeric import array_equal
from pygad.gann.gann import GANN, population_as_matrices, population_as_vectors
from pygad.nn.nn import DenseLayer, predict
from pygad import GA
from pygame import font
from food import Food
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, KEYDOWN
from pygame.time import Clock
from snake import Snake
from constants import *
import pygame
from pygame import Surface, draw
import numpy as np
if not AI_PLAYING:
    pygame.init()
    pygame.display.set_caption("Snake Game")
    screen: Surface = pygame.display.set_mode((WIDTH, HEIGH))

    text_font = font.SysFont("arial", 16)

GANN_instance = GANN(
    num_neurons_input=4,
    num_neurons_output=4,
    output_activation='sigmoid',
    hidden_activations=['relu', 'relu'],
    num_neurons_hidden_layers=[16, 16],
    num_solutions=2000

)


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


def fitness_func(solution, sol_idx):
    global GANN_instance

    current_pop: DenseLayer = GANN_instance.population_networks[sol_idx]

    score = game_loop_withou_ui(current_pop, snake=Snake(
        direction=Direction.LEFT), food=Food())

    return score


def callback_generation(ga_instance: GA):
    population_matices = population_as_matrices(
        population_networks=GANN_instance.population_networks,
        population_vectors=ga_instance.population
    )

    GANN_instance.update_population_trained_weights(
        population_trained_weights=population_matices)

    print()
    print(f'Generation: {ga_instance.generations_completed}')
    print(f'Accuracy: {ga_instance.best_solution()[1]}')
    print(f'Max score: {get_max_score()}')


def set_max_score(max: int):
    with open("max_score.pkl", "rb") as f:
        max_score = pickle.load(f)
    max_score = max
    with open("max_score.pkl", "wb") as f:
        pickle.dump(max_score, f)


def get_max_score():
    with open("max_score.pkl", "rb") as f:
        return pickle.load(f)


def game_loop(population: DenseLayer = None, ai_playing: bool = AI_PLAYING, snake: Snake = Snake(), food: Food = Food()) -> bool:
    clock = Clock()

    running = True
    gameover = False

    snake.look_around(food)

    while running:
        screen.fill(BLACK)

        if running:
            for event in pygame.event.get():
                if not ai_playing:
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == KEYDOWN:
                        snake.change_direction(event.key)
            if ai_playing:
                dir = predict(population, snake.get_vision_data())

                if dir[0] == 0:
                    snake.change_direction(K_LEFT)
                if dir[0] == 1:
                    snake.change_direction(K_RIGHT)
                if dir[0] == 2:
                    snake.change_direction(K_UP)
                if dir[0] == 3:
                    snake.change_direction(K_DOWN)

            show_score(screen, snake.score)

            snake.update(screen, show_vision=True)
            food.update(screen)

        if not ai_playing:
            while gameover == True:
                screen.fill(BLACK)
                show_score(screen, snake.score)
                show_gameover(screen)
                for event in pygame.event.get():
                    if not ai_playing:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                                running = False
                                gameover = False
                            if event.key == pygame.K_f:
                                game_loop()
                pygame.display.update()

        if running:
            if not snake.is_dead():
                snake.look_around(food)

                if snake.pos() == food.pos():
                    snake.eat()
                    food = Food()
            else:
                gameover = True
                break
        if not ai_playing:
            clock.tick(15)

        pygame.display.update()

    if ai_playing:
        max_score = get_max_score()
        max_score = snake.score if snake.score > max_score else max_score
        set_max_score(max_score)

    return snake.get_fitness()


def game_loop_withou_ui(population: DenseLayer = None, ai_playing: bool = AI_PLAYING, snake: Snake = Snake(), food: Food = Food()) -> bool:
    running = True

    snake.look_around(food)

    while running:

        if running:
            if ai_playing:
                dir = predict(population, snake.get_vision_data())

                if dir[0] == 0:
                    snake.change_direction(K_LEFT)
                if dir[0] == 1:
                    snake.change_direction(K_RIGHT)
                if dir[0] == 2:
                    snake.change_direction(K_UP)
                if dir[0] == 3:
                    snake.change_direction(K_DOWN)

            snake.update(draw=False)

        if running:
            if not snake.is_dead():
                snake.look_around(food)

                if snake.pos() == food.pos():
                    snake.eat()
                    food = Food()
            else:
                break

    if ai_playing:
        max_score = get_max_score()
        max_score = snake.score if snake.score > max_score else max_score
        set_max_score(max_score)

    return snake.get_fitness()


# TODO: implement a better way to visualize the population process
# TODO: maybe saving all the moves inside a generation folder and save each population in ur files

if __name__ == "__main__":
    if AI_PLAYING:
        population_vectors = population_as_vectors(
            population_networks=GANN_instance.population_networks)
        ga_instance = GA(num_generations=500,
                         num_parents_mating=4,
                         initial_population=population_vectors.copy(),
                         fitness_func=fitness_func,
                         mutation_percent_genes=5,
                         on_generation=callback_generation)

        ga_instance.run()
        print(get_max_score())

        print()

        ga_instance.plot_result()

        solution, solution_fitness, solution_idx = ga_instance.best_solution()

        ga_instance.save('model')

        print(solution)
        print(solution_fitness)
        print(solution_idx)

    else:
        game_loop()
