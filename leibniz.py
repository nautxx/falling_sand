import pygame
import math

# Initialize pygame
pygame.init()

# Set up the display
width, height = 1000, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pi Day Leibniz Series")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize variables
pi = 4
iterations = 0
history = [pi]  # Start history with initial value of pi
min_y = 2
max_y = 4

# Font
font = pygame.font.Font(None, 64)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Calculate denominator
    den = iterations * 2 + 3

    # Update pi value
    if iterations % 2 == 0:
        pi -= (4 / den)
    else:
        pi += (4 / den)

    # Add pi value to history
    history.append(pi)

    # Draw horizontal line representing actual value of pi
    pi_y = height - (pi - min_y) / (max_y - min_y) * height
    pygame.draw.line(screen, RED, (0, pi_y), (width, pi_y))

    # Draw curve representing history of pi values
    points = [(i * (width / len(history)), height - (value - min_y) / (max_y - min_y) * height)
              for i, value in enumerate(history)]
    
    # Draw the curve if there are at least two points
    if len(points) > 1:
        pygame.draw.lines(screen, WHITE, False, points, 2)

    # Render pi value
    pi_text = font.render(str(pi), True, WHITE)
    screen.blit(pi_text, (10, 10))

    # Update iteration count
    iterations += 1

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
