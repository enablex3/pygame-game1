import pygame
from bullet import PlayerBeam
from explosion import Explosion

class Player:

    def __init__(self):
        # define attributes
        self.size = (100, 100)
        self.velocity = 6
        self.starting_rotation = 0
        self.starting_position = (200, 700)

        # load the player's image, scale and rotate
        self.image = pygame.image.load("sprites/playerShip.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.image = pygame.transform.rotate(self.image, self.starting_rotation)

        # assign an original image for later use
        self.original_img = self.image

        # track player position
        self.rect = pygame.Rect(self.starting_position[0],
                                self.starting_position[1],
                                self.size[0],
                                self.size[1])

        # track rotation angle
        self.rotation_angle = self.starting_rotation

        # track bullets shot
        self.bullets = []

        # track health
        self.health = 5

        # track explosions
        self.explosions = []

    def update(self, keys_pressed):
        if self.rect.x > 400:
            self.rect.x = 400

        if self.rect.x < 20:
            self.rect.x = 20

        self.move(keys_pressed)

        self.explosions = [explosion for explosion in self.explosions if not explosion.should_remove()]

    def move(self, keys_pressed):
        # player only moves left or right
        if keys_pressed[pygame.K_a]:
            self.rect.x -= self.velocity

        if keys_pressed[pygame.K_d]:
            self.rect.x += self.velocity

    def add_bullet(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # fire bullet
                bullet = PlayerBeam(self.rect)
                self.bullets.append(bullet)
                return True
        return False

    def shoot(self):
        # bullets only fire to the right
        for bullet in self.bullets:
            bullet.rect.y -= bullet.velocity
            # remove bullet if passed window boundary
            if bullet.rect.y <= 60:
                self.bullets.remove(bullet)

    def detect_hit(self, enemy):
        for bullet in self.bullets:
            if bullet.rect.colliderect(enemy.rect):
                self.explosions.append(Explosion(bullet))
                self.bullets.remove(bullet)
                enemy.deplete_health()

    def deplete_health(self):
        if self.health != 0:
            self.health -= 1
        else:
            self.health = 0

