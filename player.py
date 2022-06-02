import pygame
from bullet import PlayerBeam

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

        # image to use to indicate getting hit
        self.hit_image = pygame.image.load("sprites/playerShipHit.png").convert_alpha()
        self.hit_image = pygame.transform.scale(self.hit_image, self.size)
        self.hit_image = pygame.transform.rotate(self.hit_image, self.starting_rotation)

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

        # track if hit
        self.is_hit = False
        self.is_hit_timer = None

    def update(self, keys_pressed):
        if self.rect.x > 400:
            self.rect.x = 400

        if self.rect.x < 20:
            self.rect.x = 20

        self.move(keys_pressed)

        if not self.is_hit_timer is None:
            seconds = (pygame.time.get_ticks() - self.is_hit_timer) / 1000
            if seconds >= 0.25:
                self.image = self.original_img

    def move(self, keys_pressed):
        # player only moves left or right
        if keys_pressed[pygame.K_a]:
            self.rect.x -= self.velocity

        if keys_pressed[pygame.K_d]:
            self.rect.x += self.velocity

    def add_bullet(self, keys_pressed):
        if keys_pressed[pygame.K_SPACE]:
            # fire bullet
            bullet = PlayerBeam(self.rect)
            self.bullets.append(bullet)
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("sfx/shoot.wav"))
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
                self.bullets.remove(bullet)
                enemy.deplete_health()
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("sfx/hit.wav"))

    def deplete_health(self):
        if self.health != 0:
            self.health -= 1
        else:
            self.health = 0

        self.image = self.hit_image
        self.is_hit_timer = pygame.time.get_ticks()
