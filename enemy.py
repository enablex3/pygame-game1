import random
import pygame
from bullet import EnemyBullet
from explosion import EnemyExplosion
from gametext import EnemyHealthLabel, EnemyHealthIndicator

STARTING_ROTATION = 180

SIZE = (100, 100)

STARTING_Y_OPTIONS = [80, 120]

class Enemy:

    def __init__(self):
        # define attributes
        self.velocity = random.randrange(-6, 6)
        self.starting_x = random.randrange(40, 400)
        self.starting_y = random.choice(STARTING_Y_OPTIONS)
        self.starting_position = (self.starting_x, self.starting_y)

        # load the player's image
        self.image = pygame.image.load("sprites/enemyShip.png")
        self.image = pygame.transform.scale(self.image, SIZE)
        self.image = pygame.transform.rotate(self.image, STARTING_ROTATION)

        # assign an original image for later use
        self.original_img = self.image

        # image to use to indicate getting hit
        self.hit_image = pygame.image.load("sprites/enemyShipHit.png").convert_alpha()
        self.hit_image = pygame.transform.scale(self.hit_image, SIZE)
        self.hit_image = pygame.transform.rotate(self.hit_image, STARTING_ROTATION)

        # track player position
        self.rect = pygame.Rect(self.starting_position[0],
                                self.starting_position[1],
                                SIZE[0],
                                SIZE[1])

        # track rotation angle
        self.rotation_angle = STARTING_ROTATION

        # track bullets shot
        self.bullets = []

        # track random travel time
        self.travel_time = random.randrange(1, 2)
        self.travel_start_ticks = pygame.time.get_ticks()

        # track random shooting time
        self.shooting_time = random.randrange(1, 6)
        self.shooting_start_ticks = pygame.time.get_ticks()

        # track health
        self.health = 3
        self.health_label = EnemyHealthLabel(self)
        self.health_indicator = EnemyHealthIndicator(self.health, self.health_label)

        # track explosions
        self.explosions = []

        # track if hit
        self.is_hit = False
        self.is_hit_timer = None

    def update(self):
        # keep enemies with window boundaries
        if self.rect.x > 400:
            self.rect.x = 400

        if self.rect.x < 20:
            self.rect.x = 20

        self.move()

        self.health_label.update(self)
        self.health_indicator.update(self.health, self.health_label)

        if not self.is_hit_timer is None:
            seconds = (pygame.time.get_ticks() - self.is_hit_timer) / 1000
            if seconds >= 0.25:
                self.image = self.original_img

    def move(self):
        # player only moves left or right for a random duration
        seconds = (pygame.time.get_ticks() - self.travel_start_ticks) / 1000

        # enemies move at random range of time
        if seconds > self.travel_time:
            self.travel_time = random.randrange(1, 2)
            self.travel_start_ticks = pygame.time.get_ticks()
            self.velocity = random.randrange(-5, 5)
        else:
            self.rect.x += self.velocity

    def add_bullet(self):
        # enemies shoot randomly
        seconds = (pygame.time.get_ticks() - self.shooting_start_ticks) / 1000
        if seconds > self.shooting_time:
            # fire bullet
            bullet = EnemyBullet(self.rect)
            self.bullets.append(bullet)

            self.shooting_time = random.randrange(1, 6)
            self.shooting_start_ticks = pygame.time.get_ticks()

            pygame.mixer.Channel(0).play(pygame.mixer.Sound("sfx/shoot.wav"))

            return True

        return False

    def shoot(self):
        # bullets only fire down
        for bullet in self.bullets:
            bullet.rect.y += bullet.velocity
            # remove bullet if passed window boundary
            if bullet.rect.y >= 750:
                self.bullets.remove(bullet)

    def detect_hit(self, player):
        for bullet in self.bullets:
            if bullet.rect.colliderect(player.rect):
                self.bullets.remove(bullet)
                player.deplete_health()
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("sfx/hit.wav"))

    def deplete_health(self):
        self.health -= 1
        self.image = self.hit_image
        self.is_hit_timer = pygame.time.get_ticks()
