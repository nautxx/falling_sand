import pygame
import random
import numpy as np

# constants
width, height = 800, 800
hue_value = 200
gravity = 0.2
w = 5
cols = width // w
rows = height // w

def make_2d_array(cols, rows):
    arr = np.zeros((cols, rows), dtype=int)
    return arr

def within_cols(i):
    return 0 <= i <= cols - 1

def within_rows(j):
    return 0 <= j <= rows - 1

def draw(screen):
    global hue_value, velocity_grid, cols, rows, gravity, w

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0]:
        mouse_col = mouse_x // w
        mouse_row = mouse_y // w
        matrix = 5
        extent = matrix // 2
        for i in range(-extent, extent + 1):
            for j in range(-extent, extent + 1):
                if random.random() < 0.75:
                    col = mouse_col + i
                    row = mouse_row + j
                    if within_cols(col) and within_rows(row):
                        grid[col][row] = hue_value
                        velocity_grid[col][row] = 1
        hue_value += 0.5
        if hue_value > 360:
            hue_value = 1

    for i in range(cols):
        for j in range(rows):
            if grid[i][j] > 0:
                hue = grid[i][j] % 360
                color = pygame.Color(0)
                color.hsla = (hue, 100, 50, 100)
                pygame.draw.rect(screen, color, (i * w, j * w, w, w))

    next_grid = make_2d_array(cols, rows)
    next_velocity_grid = make_2d_array(cols, rows)

    for i in range(cols):
        for j in range(rows):
            state = grid[i][j]
            velocity = velocity_grid[i][j]
            moved = False
            if state > 0:
                new_pos = int(min(max(j + velocity, 0), rows - 1))
                for y in range(new_pos, j, -1):
                    below = grid[i][y]
                    dir = 1 if random.random() < 0.5 else -1
                    below_a = grid[i + dir][y] if within_cols(i + dir) else -1
                    below_b = grid[i - dir][y] if within_cols(i - dir) else -1

                    if below == 0:
                        next_grid[i][y] = state
                        next_velocity_grid[i][y] = velocity + gravity
                        moved = True
                        break

                    elif below_a == 0:
                        next_grid[i + dir][y] = state
                        next_velocity_grid[i + dir][y] = velocity + gravity
                        moved = True
                        break

                    elif below_b == 0:
                        next_grid[i - dir][y] = state
                        next_velocity_grid[i - dir][y] = velocity + gravity
                        moved = True
                        break

            if state > 0 and not moved:
                next_grid[i][j] = grid[i][j]
                next_velocity_grid[i][j] = velocity_grid[i][j] + gravity

    grid[:] = next_grid
    velocity_grid[:] = next_velocity_grid

def main():
    global grid, velocity_grid

    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Sand Simulation")
    
    # create the grids
    grid = make_2d_array(cols, rows)
    velocity_grid = make_2d_array(cols, rows)

    # start the game loop
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
        # set background color
        screen.fill((0, 0, 0))

        # draw elements on the screen
        draw(screen)

        # update the display
        pygame.display.flip()

        # cap the frame rate
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
