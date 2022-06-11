import pygame
from force_field import ForceField
from beam.beam import PlayerBeam
from player.missile import PlayerMissile

class Player:

    def __init__(self, ship):
        # define attributes
        self.size = (80, 80)
        self.velocity = 4
        self.starting_rotation = 0
        self.starting_position = (200, 700)

        # load the player's image, scale and rotate
        self.image = pygame.image.load(ship["original_img"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.image = pygame.transform.rotate(self.image, self.starting_rotation)

        # assign an original image for later use
        self.original_img = self.image

        # image to use to indicate getting hit
        self.hit_image = pygame.image.load(ship["hit_img"]).convert_alpha()
        self.hit_image = pygame.transform.scale(self.hit_image, self.size)
        self.hit_image = pygame.transform.rotate(self.hit_image, self.starting_rotation)

        # TODO apply to all ships
        self.right_img = pygame.image.load("sprites/player/ships/blue_angel/right_turn.png").convert_alpha()
        self.right_img = pygame.transform.scale(self.right_img, self.size)
        self.left_img = pygame.image.load("sprites/player/ships/blue_angel/left_turn.png").convert_alpha()
        self.left_img = pygame.transform.scale(self.left_img, self.size)

        # define beam attributes
        self.size = (40, 40)
        self.rotation = 0
        # beam image
        self.beam_img = pygame.image.load(ship["beam_img"]).convert_alpha()
        self.beam_img = pygame.transform.scale(self.beam_img, self.size)
        self.bean_img = pygame.transform.rotate(self.beam_img, self.rotation)

        # track player position
        self.rect = pygame.Rect(self.starting_position[0],
                                self.starting_position[1],
                                self.size[0] + 20,
                                self.size[1])

        # track rotation angle
        self.rotation_angle = self.starting_rotation

        # track bullets shot
        self.bullets = []

        # track missles
        self.missiles = []

        # track health
        self.starting_health = 5
        self.health = self.starting_health

        # track if hit
        self.is_hit = False
        self.is_hit_timer = None

        # lives indicator
        self.lives_img = pygame.image.load("sprites/PlayerLivesIndicator.png")
        self.lives_img = pygame.transform.scale(self.lives_img, (20, 20))

        # force field
        self.force_field = ForceField(self.rect)
        self.force_field_timer = None
        self.force_field_show = False

    def update(self, keys_pressed):
        if self.rect.x > 400:
            self.rect.x = 400

        if self.rect.x < 20:
            self.rect.x = 20

        if self.rect.y > 700:
            self.rect.y = 700

        if self.rect.y < 200:
            self.rect.y = 200

        self.move(keys_pressed)

        if not self.is_hit_timer is None:
            seconds = (pygame.time.get_ticks() - self.is_hit_timer) / 1000
            if seconds >= 0.25:
                self.image = self.original_img
                self.is_hit_timer = None

        if not self.force_field_timer is None:
            seconds = (pygame.time.get_ticks() - self.force_field_timer) / 1000
            if seconds > 5:
                self.force_field_show = False
                self.force_field_timer = None
                self.force_field.strength = 3

        self.force_field.update(self.rect)

        if self.force_field.strength == 0:
            self.force_field_show = False
            self.force_field_timer = None
            self.force_field.strength = 3

    def move(self, keys_pressed):
        # player only moves left or right
        if keys_pressed[pygame.K_a]:
            self.rect.x -= self.velocity
            self.image = self.left_img

        if keys_pressed[pygame.K_d]:
            self.rect.x += self.velocity
            self.image = self.right_img

        if keys_pressed[pygame.K_w]:
            self.rect.y -= self.velocity

        if keys_pressed[pygame.K_s]:
            self.rect.y += self.velocity

    def add_bullet(self, sfx_enabled_setting):
        bullet = PlayerBeam(self.rect, self.beam_img)
        self.bullets.append(bullet)

        if sfx_enabled_setting:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("../sfx/shoot.wav"))

    def add_missile(self):
        missile = PlayerMissile(self.rect)
        self.missiles.append(missile)

    def shoot_missile(self):
        for missile in self.missiles:
            missile.rect.y -= missile.velocity

            if missile.rect.y <= 60:
                self.missiles.remove(missile)

    def show_force_field(self):
        if self.force_field_timer is None:
            self.force_field_show = True
            self.force_field_timer = pygame.time.get_ticks()

    def shoot(self):
        # bullets only fire to the right
        for bullet in self.bullets:
            bullet.rect.y -= bullet.velocity
            # remove bullet if passed window boundary
            if bullet.rect.y <= 60:
                self.bullets.remove(bullet)

    def detect_hit(self, enemy, sfx_enabled_setting):
        for bullet in self.bullets:
            if bullet.rect.colliderect(enemy.rect):
                self.bullets.remove(bullet)
                enemy.deplete_health(1)
                if sfx_enabled_setting:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("../sfx/hit.wav"))

        for missile in self.missiles:
            if missile.rect.colliderect(enemy.rect):
                self.missiles.remove(missile)
                enemy.deplete_health(3)

    def deplete_health(self):
        if self.health != 0:
            self.health -= 1
        else:
            self.health = 0

        self.image = self.hit_image
        self.is_hit_timer = pygame.time.get_ticks()

    def add_life(self):
        # need to add one life this way b/c the function gets called each frame
        diff = self.starting_health - self.health

        if diff == 0:
            self.health = self.starting_health
        else:
            # this keeps us from modifying self.health before adding 1
            self.health = (self.starting_health - diff) + 1

