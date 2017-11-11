import pygame
import random

# Define some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400

class Block(pygame.sprite.Sprite):
    """
    This class represents the ball. Derived from Sprite class in pygame (Child class)
    """
    def __init__(self):
        """ Constructor. Pass color of block, and position"""

        # Call the parent class (sprite) constructor
        super().__init__()
        # Create image of block and fill with color.
        self.image = pygame.Surface([20, 20])
        self.image.fill(GREEN)

        # Fetch rectangle object that has dimensions of image. Update position of object by setting values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

    def update(self):
        """Called each frame"""
        # Move block down 1 pixel
        self.rect.y += 1
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = random.randrange(-100,-10)
            self.rect.x = random.randrange(0, SCREEN_WIDTH)

class Player(pygame.sprite.Sprite):
    """ This represents player"""
    def __init__(self):
        super().__init__()
        # Create red player
        self.image = pygame.Surface([20, 15])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        # self.rect.y = pos[1] Fixed position

class Bullet(pygame.sprite.Sprite):
    """ Represents the bullet """
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([4,10])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 3


class Game(object):
    """
    This represents instance of game. If we need to reset then create new class
    """

    def __init__(self):
        """ Constructor to create our attributes and initialise game"""

        self.score = 0
        self.game_over = False
        # Create sprite lists
        self.block_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()

        # Create the block sprites
        for i in range(50):
            block = Block()
            block.rect.x = random.randrange(SCREEN_WIDTH)
            block.rect.y = random.randrange(-300, SCREEN_HEIGHT)

            self.block_list.add(block)
            self.all_sprites_list.add(block)

        self.player = Player()
        self.all_sprites_list.add(self.player)
        self.player.rect.y = 370

    def process_events(self):
        """ Process all events. Return True if we need to close window"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet()
                bullet.rect.x = self.player.rect.x + 10  # Middle of player
                bullet.rect.y = self.player.rect.y
                # Add bullet to lists
                self.all_sprites_list.add(bullet)
                self.bullet_list.add(bullet)
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    self.__init__()

        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It updates positions and checks for collisions
        """
        if not self.game_over:
            # Move spites
            self.all_sprites_list.update()

            # Check collisions of player


            # Check list of collisions
            for bullet in self.bullet_list:
                self.block_hit_list = pygame.sprite.spritecollide(bullet, self.block_list, True)
                # player_collision = pygame.sprite.spritecollide(self.player, self.block_list, True)

                for block in self.block_hit_list:
                    self.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)
                    self.score += 1
                    print(self.score)
                    # Do something with block?

                if bullet.rect.y < -10:
                    self.bullet_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)

            if len(self.block_list) == 0:
                self.game_over = True

    def display_frame(self, screen):
        """ Display everything """
        screen.fill(WHITE)

        if self.game_over:
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, Click to restart", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if not self.game_over:
            self.all_sprites_list.draw(screen)

        pygame.display.flip()

def main():
    """ Main Program function """
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    pygame.display.set_caption("Sprite Collisions")
    pygame.mouse.set_visible(False)

    done = False
    clock = pygame.time.Clock()

    game = Game()

# --- Main Program ---
    while not done:
        # Process events
        done = game.process_events()

        # Update object positions and check collisions
        game.run_logic()

        game.display_frame(screen)

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()