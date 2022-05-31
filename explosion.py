import pygame

class Explosion:

    def __init__(self, enemy):
        # define attributes
        self.size = (20, 20)

        # load the image and scale
        self.image = pygame.image.load("sprites/explosion.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        # track the position
        self.rect = enemy.rect

        # track time
        self.starting_display_time = pygame.time.get_ticks()

    # function to check how long the explosion has been displayed
    def should_remove(self):
        seconds = (pygame.time.get_ticks() - self.starting_display_time) / 1000
        if seconds > 0.5:
            return True
