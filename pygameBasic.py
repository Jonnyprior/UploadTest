import pygame

pygame.init()


# Define some colours

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set width and height of screen
size = (700, 500)
Main_screen = pygame.display.set_mode(size)

pygame.display.set_caption("Main Screen")

# Loop until user clicks close button
done = False

# Used to manage how fast screen updates
clock = pygame.time.Clock()

# ----- Main Program loop -----
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If user clicks close
            done = True

    Main_screen.fill(WHITE)

    pygame.draw.line(Main_screen, GREEN, [0, 0], [100,100], 5)

    pygame.display.flip()

    # Set window to 60 fps
    clock.tick(60)
# Close the window and quit
pygame.quit()