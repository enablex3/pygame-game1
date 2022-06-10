import pygame

class PlayerMissile:

    def __init__(self, player_rect):
        self.size = (20, 50)
        self.velocity = 4

        self.img = pygame.image.load("sprites/playerMissle.png")
        self.img = pygame.transform.scale(self.img, self.size)

        self.rect = pygame.Rect(
            player_rect.x + 25,
            player_rect.y + player_rect.height // 2 - 2,
            self.size[0],
            self.size[1]
        )

