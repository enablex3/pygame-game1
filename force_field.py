import pygame

SIZE = (110, 110)

class ForceField:

    def __init__(self, player_rect):
        self.img = pygame.image.load("sprites/ForceField.png")
        self.img = pygame.transform.scale(self.img, SIZE)

        self.original_img = self.img

        self.hit_img = pygame.image.load("sprites/ForceFieldHit.png")
        self.hit_img = pygame.transform.scale(self.hit_img, SIZE)

        self.offset_x = 15
        self.offset_y = 35

        self.rect = pygame.Rect(
            player_rect.x - self.offset_x,
            player_rect.y + player_rect.height // 2 - self.offset_y,
            SIZE[0],
            SIZE[1])

        self.strength = 3

        self.is_hit_timer = None

    def update(self, player_rect):
        self.rect = pygame.Rect(
            player_rect.x - self.offset_x,
            player_rect.y + player_rect.height // 2 - self.offset_y,
            SIZE[0],
            SIZE[1])

        if not self.is_hit_timer is None:
            seconds = (pygame.time.get_ticks() - self.is_hit_timer) / 1000
            if seconds >= 0.25:
                self.img = self.original_img

    def deplete_strength(self):
        self.strength -= 1

        self.img = self.hit_img
        self.is_hit_timer = pygame.time.get_ticks()
