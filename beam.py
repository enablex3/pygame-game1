import pygame

class PlayerBeam:

    def __init__(self, player_rect, beam_img):
        # assign beam image
        self.image = beam_img

        # velocity
        self.velocity = 10

        # track the position
        self.rect = pygame.Rect(
            player_rect.x + 15,
            player_rect.y + player_rect.height // 2 - 50,
            10,
            5
        )

        # track if should be displayed
        self.should_show = True

        # bullet explosion (None at init)
        self.explosion = None

class EnemyBeam:

    def __init__(self, player_rect, size, x_add, y_add):
        # define attributes
        self.size = size
        self.velocity = 10
        self.rotation = 180

        # load the image and scale
        self.image = pygame.image.load("sprites/enemyBeam.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.image = pygame.transform.rotate(self.image, self.rotation)

        # track the position
        self.rect = pygame.Rect(
            player_rect.x + x_add,
            player_rect.y + player_rect.height // 2 + y_add,
            10,
            5
        )

        # track if should be displayed
        self.should_show = True

        # bullet explosion (None at init)
        self.explosion = None
