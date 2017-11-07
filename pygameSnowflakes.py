import pygame
import random

# Define some colours

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BALL_SIZE = 25
SCREEN_SIZE = [SCREEN_WIDTH, SCREEN_HEIGHT]

Main_screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Snow Animation")

snow_list = []

# Loop 50 times to add snowflakes in random positions
for i in range(50):
    x = random.randrange(0, SCREEN_WIDTH)
    y = random.randrange(0, SCREEN_HEIGHT)
    snow_list.append([x, y])

clock = pygame.time.Clock()

done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    Main_screen.fill(BLACK)

    # Process each snowflake in list
    for item in snow_list:
        # Draw snowflake
        item[1] += 1 # Move snowflake down y column
        pygame.draw.circle(Main_screen, WHITE, item, 2)

        # If snowflake moved off the bottom of screen
        if item[1] > SCREEN_HEIGHT:
            # Reset to above top
            item[1] = random.randrange(-20, -5)

            # Give new x position
            item[0] = random.randrange(0, SCREEN_WIDTH)

    # Update screen
    pygame.display.flip()
    clock.tick(20)

pygame.quit()