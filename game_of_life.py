import sys
import os
import pygame
import numpy as np
from cell_state import CellState

GAME_NAME = 'Game of Life'
GRID_BACKGROUND_COLOR = (30, 30, 60)
CELL_DEAD_COLOR = (10, 10, 40)
CELL_ABOUT_TO_DIE_COLOR = (253, 255, 182)
CELL_ALIVE_COLOR = (153, 217, 140)

CELL_COLORS_BY_STATE = {CellState.DEAD: CELL_DEAD_COLOR,
                        CellState.ABOUT_TO_DIE: CELL_ABOUT_TO_DIE_COLOR,
                        CellState.ALIVE: CELL_ALIVE_COLOR}


def main(number_of_lines, number_of_columns, cell_size_in_pixels):
    print(f'Starting {GAME_NAME}...')
    pygame.init()

    surface = create_game_surface(number_of_lines, number_of_columns, cell_size_in_pixels)
    pygame.display.set_caption(GAME_NAME)

    cells = init_cells_randomly(number_of_lines, number_of_columns)

    run_game_loop(cells, surface, cell_size_in_pixels)


def create_game_surface(number_of_lines, number_of_columns, cell_size_in_pixels):
    return pygame.display.set_mode((number_of_columns * cell_size_in_pixels, number_of_lines * cell_size_in_pixels))


def init_cells_randomly(number_of_lines, number_of_columns):
    cells = np.random.randint(CellState.DEAD.value, CellState.NONE.value, (number_of_lines, number_of_columns))
    return cells


def get_cell_color(cell_state):
    return CELL_COLORS_BY_STATE[cell_state]


def draw_cells(cells, surface, cell_size_in_pixels):
    for line, column in np.ndindex(cells.shape):
        cell_state = CellState(cells[line, column])
        pygame.draw.rect(surface, get_cell_color(cell_state),
                         get_cell_rectangle(line, column, cell_size_in_pixels))


def get_cell_rectangle(line, column, cell_size_in_pixels):
    cell_start_position_x = column * cell_size_in_pixels
    cell_start_position_y = line * cell_size_in_pixels
    cell_width = cell_size_in_pixels - 1
    return cell_start_position_x, cell_start_position_y, cell_width, cell_width


def count_number_of_cells_alive_around(cells, line, column):
    cells_around = cells[line - 1:line + 2, column - 1:column + 2]
    count = 0
    for cell_line, cell_column in np.ndindex(cells_around.shape):
        if CellState(cells_around[cell_line, cell_column]) == CellState.ALIVE:
            count = count + 1

    if CellState(cells[line, column]) == CellState.ALIVE:
        count = count - 1

    return count


def compute_next_cell_generation(current_generation):
    next_generation = np.zeros((current_generation.shape[0], current_generation.shape[1]))

    for line, column in np.ndindex(current_generation.shape):
        nb_cells_alive = count_number_of_cells_alive_around(current_generation, line, column)
        cell_state = CellState(current_generation[line, column])

        if cell_state == CellState.ALIVE and nb_cells_alive < 2 or nb_cells_alive > 3:
            next_generation[line, column] = CellState.ABOUT_TO_DIE.value
        elif (cell_state == CellState.ALIVE and 2 <= nb_cells_alive <= 3) or (
                cell_state == CellState.DEAD and nb_cells_alive == 3):
            next_generation[line, column] = CellState.ALIVE.value

    return next_generation


def draw(cells, surface, cell_size_in_pixels):
    surface.fill(GRID_BACKGROUND_COLOR)
    draw_cells(cells, surface, cell_size_in_pixels)
    pygame.display.update()


def run_game_loop(cells, surface, cell_size_in_pixels):
    draw(cells, surface, cell_size_in_pixels)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print(f'Exited {GAME_NAME}')
                sys.exit(os.EX_OK)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    cells = compute_next_cell_generation(cells)
                    draw(cells, surface, cell_size_in_pixels)


if __name__ == "__main__":
    main(50, 70, 15)
