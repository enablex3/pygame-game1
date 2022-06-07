import pygame
import random

class Asteroid:

    def __init__(self):
        self.velocity = 2
        self.rotation_speed = 2
        self.material = random.choice(["COOLANT", "LIFE"])
        self.size = random.choice([(40, 40), (50, 50), (60, 60), (80, 80)])
        self.starting_position = random.choice([(500, 250), (500, 180), (500, 300), (0, 250), (0, 180), (0, 300)])
        self.image = pygame.image.load("sprites/Asteroid.png")
        self.rect = pygame.Rect(self.starting_position[0],
                                self.starting_position[1],
                                self.size[0],
                                self.size[1])
        self.velocity = -2 if self.starting_position[0] == 500 else 2

    def update(self):
        self.rect.x += self.velocity
