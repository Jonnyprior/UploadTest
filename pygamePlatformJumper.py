import pygame


# Define some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    """ Represents the bar at bottom of player """

    def __init__(self):
        super().__init__()

        # Create image of block and fill.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        # Set a reference to image rect
        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0

        self.level = None

    def update(self):
        """ Move player """
        # Gravity
        self.calc_grav()

        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x

    def calc_grav(self):
        """ Calculate effect of gravity. Bigger means more grav, accelerating so += """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on ground
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits up arrow """

        # Move down temporarily to see if platform below us.
        # Move 2 pixels as works better when moving platform
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is okay to jump, set speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10


    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class MovingPlatform(Platform):
    """ This is a fancier platform that can move """
    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    player = None
    level = None

    def update(self):
        """ Move the platform
        If player in way, it will shove player. Does deal with if player pushed into another object
        Make sure platform has clearance or add code to handle """

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We hit player so shove it. Assume nothing in way

            # If moving right, set out right side to left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else
            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        # Check boundaries and see if we need to reverse direction
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1

class Level(object):
    """ Generic super-class used to define a level.
    Create child class for each level, with specific info """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player.
        Needed for when moving platforms collide with player """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        self.background = None

        self.world_shift = 0
        self.level_limit = -1000

    # Update everything on this level
    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        screen.fill(BLUE)
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        """ When user moves left/right we need to scroll everything """

        # Keep track of shift amount
        self.world_shift += shift_x

        # Go through all sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x


class Level_01(Level):
    """ Definition for level 1 """

    def __init__(self, player):
        """ Create level 1 """

        # Call parent constructor
        Level.__init__(self, player)

        self.level_limit = -1500

        # Array with width, height, x, and y of platform
        level = [[210, 70, 500, 500],
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1120, 280],
                 ]

        # Go through array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player # Need reference to player to know where it is on moving block
            self.platform_list.add(block)

        # Add a custom moving platform
        block = MovingPlatform(70, 40)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000

        # Array with type of platform, and x, y location of the platform.
        level = [[210, 70, 500, 550],
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1120, 280],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = MovingPlatform(70, 70)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


def main():
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Moving Platform Jumper")

    player = Player()

    level_list = []
    level_list.append( Level_01(player))
    level_list.append(Level_02(player))

    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    done = False

    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # Update player
        active_sprite_list.update()

        current_level.update()

        # If player gets near the right side then shift world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)

        # Left side
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)

        # If player gets to end of level, go to next
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            if current_level_no < len(level_list) -1:
                player.rect.x = 120
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
            else:
                # Out of levels. Exits program
                # You'll want to do something better
                done = True

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()