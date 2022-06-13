import random
import pygame
from beam.beam import EnemyBeam

STARTING_ROTATION = 180

SIZE = (100, 100)

STARTING_Y_OPTIONS = [80, 120]

class Apache:

    def __init__(self, window_width, window_height):
        # define attributes
        self.velocity = 6
        self.starting_x = random.randrange(40, 400)
        self.starting_y = random.choice(STARTING_Y_OPTIONS)
        self.starting_position = (self.starting_x, self.starting_y)

        # load the player's image
        self.image = pygame.image.load("sprites/enemies/ships/apache/original.png")
        self.image = pygame.transform.scale(self.image, SIZE)
        self.image = pygame.transform.rotate(self.image, STARTING_ROTATION)

        # assign an original image for later use
        self.original_img = self.image

        # image to use to indicate getting hit
        self.hit_image = pygame.image.load("sprites/enemies/ships/apache/original_hit.png").convert_alpha()
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
        self.beam_size = (60, 60)

        # track random travel time
        self.travel_time = random.randrange(3, 5)
        self.travel_start_ticks = pygame.time.get_ticks()

        # track random shooting time
        self.shooting_time = random.randrange(1, 2)
        self.shooting_start_ticks = pygame.time.get_ticks()

        # track health
        self.health = 12

        # boundary definitions
        self.boundary_x = [SIZE[0], window_width - SIZE[0]]
        self.boundary_y = [SIZE[1] // 2, window_height - SIZE[1]]

        # track explosions
        self.explosions = []

        # track if hit
        self.is_hit = False
        self.is_hit_timer = None

        # random directions
        self.directions = ["x", "y", "xy", "-x", "-y", "-xy"]

    def update(self):
        # keep enemies with window boundaries
        if self.rect.x > self.boundary_x[1]:
            self.rect.x = self.boundary_x[1]

        if self.rect.x < self.boundary_x[0]:
            self.rect.x = self.boundary_x[0]

        if self.rect.y > self.boundary_y[1]:
            self.rect.y = self.boundary_y[1]

        if self.rect.y < self.boundary_y[0]:
            self.rect.y = self.boundary_y[0]

        self.move()

        if not self.is_hit_timer is None:
            seconds = (pygame.time.get_ticks() - self.is_hit_timer) / 1000
            if seconds >= 0.25:
                self.image = self.original_img

    def move(self):
        # player only moves left or right for a random duration
        seconds = (pygame.time.get_ticks() - self.travel_start_ticks) / 1000
        direction = random.choice(self.directions)

        # enemies move at random range of time
        if seconds > self.travel_time:
            self.travel_time = random.randrange(3, 5)
            self.travel_start_ticks = pygame.time.get_ticks()
        else:
            if direction == "x":
                self.rect.x += self.velocity
            if direction == "y":
                self.rect.y += self.velocity
            if direction == "xy":
                self.rect.y += self.velocity
                self.rect.x += self.velocity
            if direction == "-x":
                self.rect.x -= self.velocity
            if direction == "-y":
                self.rect.y -= self.velocity
            if direction == "-xy":
                self.rect.y -= self.velocity
                self.rect.x -= self.velocity

    def add_bullet(self, sfx_enabled_setting):
        # enemies shoot randomly
        seconds = (pygame.time.get_ticks() - self.shooting_start_ticks) / 1000
        if seconds > self.shooting_time:
            # fire 3 bullets
            self.bullets.append(EnemyBeam(self.rect, self.beam_size, 40, 30))
            self.bullets.append(EnemyBeam(self.rect, self.beam_size, 0, 30))
            self.bullets.append(EnemyBeam(self.rect, self.beam_size, 80, 30))

            self.shooting_time = random.randrange(1, 2)
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
            if bullet.rect.colliderect(player.rect):
                self.bullets.remove(bullet)
                player.deplete_health()
                if sfx_enabled_setting:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("sfx/hit.wav"))

    def deplete_health(self, amount):
        self.health -= amount
        self.image = self.hit_image
        self.is_hit_timer = pygame.time.get_ticks()
