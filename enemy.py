import random
import pygame
from beam import EnemyBeam

STARTING_ROTATION = 180

SIZE = (60, 60)

STARTING_Y_OPTIONS = [80, 120]

class Enemy:

    def __init__(self, shot_frequency, velocity):
        # define attributes
        self.velocity = random.randrange(-velocity, velocity)
        self.shot_frequency = shot_frequency
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
                                SIZE[0] + 20,
                                SIZE[1])

        # track rotation angle
        self.rotation_angle = STARTING_ROTATION

        # track bullets shot
        self.bullets = []
        self.beam_size = (40, 40)

        # track random travel time
        self.travel_time = random.randrange(1, 2)
        self.travel_start_ticks = pygame.time.get_ticks()

        # track random shooting time
        self.shooting_time = random.randrange(1, self.shot_frequency)
        self.shooting_start_ticks = pygame.time.get_ticks()

        # track health
        self.health = 3

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

    def add_bullet(self, sfx_enabled_setting):
        # enemies shoot randomly
        seconds = (pygame.time.get_ticks() - self.shooting_start_ticks) / 1000
        if seconds > self.shooting_time:
            # fire bullet
            bullet = EnemyBeam(self.rect, self.beam_size, 15, 20)
            self.bullets.append(bullet)

            self.shooting_time = random.randrange(1, self.shot_frequency)
            self.shooting_start_ticks = pygame.time.get_ticks()

            if sfx_enabled_setting:
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

    def detect_hit(self, player, sfx_enabled_setting):
        for bullet in self.bullets:

            if player.force_field_show:
                if bullet.rect.colliderect(player.force_field.rect):
                    self.bullets.remove(bullet)
                    player.force_field.deplete_strength()
                    if sfx_enabled_setting:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("sfx/hit.wav"))

            if not player.force_field_show:
                if bullet.rect.colliderect(player.rect):
                    self.bullets.remove(bullet)
                    player.deplete_health()
                    if sfx_enabled_setting:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("sfx/hit.wav"))

    def deplete_health(self):
        self.health -= 1
        self.image = self.hit_image
        self.is_hit_timer = pygame.time.get_ticks()
