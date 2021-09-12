from numpy.core.numeric import array_equal
from pygad.gann.gann import GANN, population_as_matrices, population_as_vectors
from pygad.nn.nn import DenseLayer, predict
from pygad import GA
from pygame import font
from food import Food
from pygame.constants import KEYDOWN
from pygame.time import Clock
from snake import Snake
from constants import *
import pygame
from pygame import Surface, draw
import numpy as np

pygame.init()
pygame.display.set_caption("Snake Game")
screen: Surface = pygame.display.set_mode((WIDTH, HEIGH))

text_font = font.SysFont("arial", 16)

data_inputs = np.array([
    [-1, 1, 0, 0],
    [1, -1, 0, 0],
])

data_outputs = np.array([
    [0, 1, 0, 0],
    [1, 0, 0, 0],
])

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

    print(data_inputs)

    predictions = predict(
        last_layer=current_pop, data_inputs=data_inputs)

    correct_predictions = np.where(
        array_equal(predictions, data_outputs))[0].size

    solution_fitness = (correct_predictions/data_outputs.size)*100

    return solution_fitness


def callback_generation(ga_instance: GA):
    population_matices = population_as_matrices(
        population_networks=GANN_instance.population_networks,
        population_vectors=ga_instance.population
    )

    GANN_instance.update_population_trained_weights(
        population_trained_weights=population_matices)

    # print(f'Generation: {ga_instance.generations_completed}')
    # print(f'Accuracy: {ga_instance.best_solution()[1]}')


def main():
    snake = Snake()
    food = Food()

    clock = Clock()

    running = True
    gameover = False
    
    while running:
        screen.fill(BLACK)

        if running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == KEYDOWN:
                    snake.change_direction(event.key)

            show_score(screen, snake.score)

            snake.update(screen, show_vision=True)
            food.draw(screen)

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
            draw.rect(screen, WHITE, [
                snake.head.x, snake.head.y, snake.head.size, snake.head.size])

            pygame.display.update()

        if running:
            if not snake.is_dead():
                snake.look_around(food)

                if snake.pos() == food.pos():
                    snake.eat()
                    food = Food()
            else:
                gameover = True
        clock.tick(15)

        pygame.display.update()


if __name__ == "__main__":
    population_vectors = population_as_vectors(
        population_networks=GANN_instance.population_networks)
    ga_instance = GA(num_generations=50,
                     num_parents_mating=10,
                     initial_population=population_vectors.copy(),
                     fitness_func=fitness_func,
                     mutation_percent_genes=5,
                     on_generation=callback_generation)

    ga_instance.run()

    main()
