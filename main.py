import pygame
import random
import numpy as np

# constants
WIDTH, HEIGHT = 800, 800
HUE_VALUE = 200
GRAVITY = 2
DIM = 4
COLS = WIDTH // DIM
ROWS = HEIGHT // DIM

def make_2d_array(COLS, ROWS):
    return np.zeros((COLS, ROWS), dtype=int)

def within_cols(i):
    return 0 <= i <= COLS - 1

def within_rows(j):
    return 0 <= j <= ROWS - 1

def draw(screen):
    global HUE_VALUE, velocity_grid

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
                    if within_cols(col) and within_rows(row):
                        grid[col][row] = HUE_VALUE
                        velocity_grid[col][row] = 1
        HUE_VALUE += 0.5
        if HUE_VALUE > 360:
            HUE_VALUE = 1

    for i in range(COLS):
        for j in range(ROWS):
            if grid[i][j] > 0:
                hue = grid[i][j] % 360
                color = pygame.Color(0)
                color.hsla = (hue, 100, 50, 100)
                pygame.draw.rect(screen, color, (i * DIM, j * DIM, DIM, DIM))

    next_grid = make_2d_array(COLS, ROWS)
    next_velocity_grid = make_2d_array(COLS, ROWS)

    for i in range(COLS):
        for j in range(ROWS):
            state = grid[i][j]
            velocity = velocity_grid[i][j]
            moved = False
            if state > 0:
                new_pos = int(min(max(j + velocity, 0), ROWS - 1))
                for y in range(new_pos, j, -1):
                    below = grid[i][y]
                    dir = 1 if random.random() < 0.5 else -1
                    below_a = grid[i + dir][y] if within_cols(i + dir) else -1
                    below_b = grid[i - dir][y] if within_cols(i - dir) else -1

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
                next_grid[i][j] = grid[i][j]
                next_velocity_grid[i][j] = velocity_grid[i][j] + GRAVITY

    grid[:] = next_grid
    velocity_grid[:] = next_velocity_grid

def main():
    global grid, velocity_grid

    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Sand Simulation")
    
    # create the grids
    grid = make_2d_array(COLS, ROWS)
    velocity_grid = make_2d_array(COLS, ROWS)

    # start the game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # set background color
        screen.fill((0, 0, 0))

        # draw elements on the screen
        draw(screen)

        # update the display
        pygame.display.flip()

        # cap the frame rate
        clock.tick(120)
    
    pygame.quit()

if __name__ == "__main__":
    main()
