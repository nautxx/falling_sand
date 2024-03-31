import pygame
import math

# constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def main():
    # Initialize pygame
    pygame.init()

    # Set up the display
    width, height = 1200, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Leibniz Formula for Pi")
    font = pygame.font.Font(None, 64)

    # Initialize variables
    pi = 4
    iterations = 0
    history = [pi]  # Start history with initial value of pi
    min_y = 2
    max_y = 4

    # main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # clear the screen
        screen.fill(WHITE)

        # calculate denominator
        den = iterations * 2 + 3

        # update pi value
        if iterations % 2 == 0:
            pi -= (4 / den)
        else:
            pi += (4 / den)

        # add pi value to history
        history.append(pi)

        # draw horizontal line representing actual value of pi
        pi_y = height - (pi - min_y) / (max_y - min_y) * height
        pygame.draw.line(screen, RED, (0, pi_y), (width, pi_y))

        # draw curve representing history of pi values
        points = [(i * (width / len(history)), height - (value - min_y) / (max_y - min_y) * height)
                for i, value in enumerate(history)]
        
        # draw the curve if there are at least two points
        if len(points) > 1:
            pygame.draw.lines(screen, BLACK, False, points, 2)

        # render pi value
        pi_text = font.render(str(pi), True, BLACK)
        screen.blit(pi_text, (10, 550))

        # update iteration count
        iterations += 1

        # update the display
        pygame.display.flip()

    # quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()