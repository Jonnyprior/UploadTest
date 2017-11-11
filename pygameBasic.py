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

class Ball:
    """Class to keep track of a balls location and vector"""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0


def make_ball():
    """Function to make a new, random ball
    """
    ball = Ball()
    # Start pos. Take into account ball size
    ball.x = random.randrange(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)
    ball.y = random.randrange(BALL_SIZE, SCREEN_HEIGHT - BALL_SIZE)

    # Speed and direction of ball
    ball.change_x = random.randrange(-2, 3)
    ball.change_y = random.randrange(-2, 3)

    return ball

def main():
    # Main program

    pygame.init()

    # Set width and height of screen
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    Main_screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Main Screen")

    # Loop until user clicks close button
    done = False

    # Used to manage how fast screen updates
    clock = pygame.time.Clock()

    ball_list = []
    ball = make_ball()
    ball_list.append(ball)

    # ----- Main Progr  am loop -----
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If user clicks close
                done = True
            elif event.type == pygame.KEYDOWN:
                # Space to spawn new ball
                if event.key == pygame.K_SPACE:
                    ball = make_ball()
                    ball_list.append(ball)


        # Logic
        for ball in ball_list:
            # Move the balls center
            ball.x += ball.change_x
            ball.y += ball.change_y

            # Bounce ball if needed
            if ball.y > SCREEN_HEIGHT - BALL_SIZE or ball.y < BALL_SIZE:
                ball.change_y *= -1
            if ball.x > SCREEN_WIDTH - BALL_SIZE or ball.x < BALL_SIZE:
                ball.change_x *= -1

        # Drawing - Updates screen after ball has moved
        Main_screen.fill(BLACK)

        # Draw balls
        for ball in ball_list:
            pygame.draw.circle(Main_screen, WHITE, [ball.x, ball.y], BALL_SIZE)

        # Set window to 60 fps
        clock.tick(60)
        pygame.display.flip()

    # Close the window and quit
    pygame.quit()

if __name__ == "__main__":
    main()