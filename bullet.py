import pygame

class PlayerBeam:

    def __init__(self, player_rect):
        # define attributes
        self.size = (40, 40)
        self.velocity = 10
        self.rotation = 0

        # load the image and scale
        self.image = pygame.image.load("sprites/playerBeam.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.image = pygame.transform.rotate(self.image, self.rotation)

        # track the position
        self.rect = pygame.Rect(
            player_rect.x + 50,
            player_rect.y + player_rect.height // 2 - 10,
            10,
            5
        )

        # track if should be displayed
        self.should_show = True

        # bullet explosion (None at init)
        self.explosion = None

class EnemyBullet:

    def __init__(self, player_rect):
        # define attributes
        self.size = (40, 40)
        self.velocity = 10
        self.rotation = 180

        # load the image and scale
        self.image = pygame.image.load("sprites/enemyBeam.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.image = pygame.transform.rotate(self.image, self.rotation)

        # track the position
        self.rect = pygame.Rect(
            player_rect.x + 50,
            player_rect.y + player_rect.height // 2 - 10,
            10,
            5
        )

        # track if should be displayed
        self.should_show = True

        # bullet explosion (None at init)
        self.explosion = None
