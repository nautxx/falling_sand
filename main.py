import pygame
import random
import numpy as np
from settings import *


class Game:
    def __init__(self):
        # initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Sand Simulation")
        
        # create the grids
        self.grid = self.make_2d_array(COLS, ROWS)
        self.velocity_grid = self.make_2d_array(COLS, ROWS)

    def make_2d_array(self, COLS, ROWS):
        return np.zeros((COLS, ROWS), dtype=int)

    def within_cols(self, i):
        return 0 <= i <= COLS - 1

    def within_rows(self, j):
        return 0 <= j <= ROWS - 1

    def draw(self):
        global HUE_VALUE

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            mouse_col = mouse_x // DIM
            mouse_row = mouse_y // DIM
            matrix = 5
            extent = matrix // 2
            for i in range(-extent, extent + 1):
                for j in range(-extent, extent + 1):
                    if random.random() < 0.75:
                        col = mouse_col + i
                        row = mouse_row + j
                        if self.within_cols(col) and self.within_rows(row):
                            self.grid[col][row] = HUE_VALUE
                            self.velocity_grid[col][row] = 1
            HUE_VALUE += 0.5
            if HUE_VALUE > 360:
                HUE_VALUE = 1

        for i in range(COLS):
            for j in range(ROWS):
                if self.grid[i][j] > 0:
                    hue = self.grid[i][j] % 360
                    color = pygame.Color(0)
                    color.hsla = (hue, 100, 50, 100)
                    pygame.draw.rect(self.screen, color, (i * DIM, j * DIM, DIM, DIM))

        next_grid = self.make_2d_array(COLS, ROWS)
        next_velocity_grid = self.make_2d_array(COLS, ROWS)

        for i in range(COLS):
            for j in range(ROWS):
                state = self.grid[i][j]
                velocity = self.velocity_grid[i][j]
                moved = False
                if state > 0:
                    new_pos = int(min(max(j + velocity, 0), ROWS - 1))
                    for y in range(new_pos, j, -1):
                        below = self.grid[i][y]
                        dir = 1 if random.random() < 0.5 else -1
                        below_a = self.grid[i + dir][y] if self.within_cols(i + dir) else -1
                        below_b = self.grid[i - dir][y] if self.within_cols(i - dir) else -1

                        if below == 0:
                            next_grid[i][y] = state
                            next_velocity_grid[i][y] = velocity + GRAVITY
                            moved = True
                            break

                        elif below_a == 0:
                            next_grid[i + dir][y] = state
                            next_velocity_grid[i + dir][y] = velocity + GRAVITY
                            moved = True
                            break

                        elif below_b == 0:
                            next_grid[i - dir][y] = state
                            next_velocity_grid[i - dir][y] = velocity + GRAVITY
                            moved = True
                            break

                if state > 0 and not moved:
                    next_grid[i][j] = self.grid[i][j]
                    next_velocity_grid[i][j] = self.velocity_grid[i][j] + GRAVITY

        self.grid[:] = next_grid
        self.velocity_grid[:] = next_velocity_grid

    def run(self):
        # start the game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            # set background color
            self.screen.fill((255, 255, 255))

            # draw elements on the screen
            self.draw()

            # update the display
            pygame.display.flip()

            # cap the frame rate
            self.clock.tick(120)
        
        pygame.quit()

if __name__ == "__main__":
    sim = Game()
    sim.run()
