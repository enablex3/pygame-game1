import pygame
import random

class Asteroid:

    def __init__(self):
        self.velocity = 2
        self.rotation_speed = 2
        self.material = random.choice(["COOLANT", "LIFE"])
        self.size = random.choice([(40, 40), (80, 80), (120, 120), (160, 160)])
        self.starting_position = random.choice([(500, 250), (500, 180), (500, 300), (0, 250), (0, 180), (0, 300)])
        self.image = pygame.image.load("asteroid/Asteroid.png")
        self.rect = pygame.Rect(self.starting_position[0],
                                self.starting_position[1],
                                self.size[0],
                                self.size[1])
        self.velocity = -2 if self.starting_position[0] == 500 else 2

    def update(self):
        self.rect.x += self.velocity
        self.rect.y += self.velocity
