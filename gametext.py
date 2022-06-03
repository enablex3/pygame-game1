import pygame

pygame.font.init()

LABEL_X = 120
LABEL_Y = 20
INDICATOR_X = LABEL_X + 50

class MenuLabel:

    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 75
        self.label = "Menu"
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (0, 0, 0))
        self.position = (150, 20)

class MusicLabel:

    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 50
        self.label = "Music: "
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (0, 0, 0))
        self.position = (10, 100)

class MusicEnable:

    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 40
        self.label = "Enable"
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (0, 255, 0))
        self.position = (130, 105)

class MusicDisable:

    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 40
        self.label = "Disable"
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (255, 0, 0))
        self.position = (240, 105)

class SFXLabel:

    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 50
        self.label = "SFX: "
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (0, 0, 0))
        self.position = (10, 150)

class SFXEnable:

    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 40
        self.label = "Enable"
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (0, 255, 0))
        self.position = (100, 155)

class SFXDisable:

    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 40
        self.label = "Disable"
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (255, 0, 0))
        self.position = (210, 155)

class LoadingLabel:

    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 50
        self.label = "Loading..."
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (0, 0, 0))
        self.position = (175, 500)

class AmmoLabel:

    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 20
        self.label = "Ammo:"
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (255, 255, 255))
        self.position = (LABEL_X, LABEL_Y)

class AmmoIndicator:

    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 20
        self.ammo = 30
        self.color = (25, 255, 124)
        self.label = str(self.ammo)
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, self.color)
        self.position = (INDICATOR_X, LABEL_Y)

    def update(self):
        if self.ammo == 1:
            self.label = "RELOAD!"
            self.color = (205, 92, 92)
        else:
            self.ammo -= 1
            self.label = str(self.ammo)
            self.color = (255, 255, 255)

        if self.ammo > 20:
            self.color = (25, 255, 124)
        elif 20 >= self.ammo > 10:
            self.color = (255, 255, 0)
        else:
            self.color = (255, 100, 100)

        self.image = self.fontObj.render(self.label, True, self.color)

    def reload(self, keys_pressed):
        if keys_pressed[pygame.K_r]:
            self.ammo = 30
            self.label = str(self.ammo)
            self.color = (25, 255, 124)
            self.image = self.fontObj.render(self.label, True, self.color)

class PlayerHealthLabel:

    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 20
        self.label = "Health:"
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (255, 255, 255))
        self.position = (LABEL_X + 80, LABEL_Y)

class PlayerHealthIndicator:

    def __init__(self, health):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 20
        self.label = str(health)
        self.color = (25, 255, 124)
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, self.color)
        self.position = (INDICATOR_X + 75, LABEL_Y)

    def update(self, health):
        if health <= 3:
            self.color = (255, 100, 100)
        else:
            self.color = (25, 255, 124)

        self.label = str(health)

        self.image = self.fontObj.render(self.label, True, self.color)

class EnemiesLabel:
    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 20
        self.label = "Enemies:"
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (255, 255, 255))
        self.position = (LABEL_X + 150, LABEL_Y)


class EnemiesIndicator:

    def __init__(self, enemies):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 20
        self.label = str(len(enemies))
        self.color = (255, 255, 255)
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, self.color)
        self.position = (INDICATOR_X + 160, LABEL_Y)

    def update(self, enemies):
        self.label = str(len(enemies))

        self.image = self.fontObj.render(self.label, True, self.color)

class WavesLabel:
    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 20
        self.label = "Wave:"
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (255, 255, 255))
        self.position = (LABEL_X + 230, LABEL_Y)


class WavesIndicator:

    def __init__(self, wave_number):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 20
        self.label = str(wave_number)
        self.color = (255, 255, 255)
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, self.color)
        self.position = (INDICATOR_X + 220, LABEL_Y)

    def update(self, wave_number):
        self.label = str(wave_number)

        self.image = self.fontObj.render(self.label, True, self.color)

class EnemyHealthLabel:

    def __init__(self, enemy):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 20
        self.label = "Health:"
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (255, 255, 255))
        self.position = (enemy.rect.x + 10, enemy.rect.y - 20)

    def update(self, enemy):
        self.position = (enemy.rect.x + 10, enemy.rect.y - 5)

class EnemyHealthIndicator:

    def __init__(self, health, enemy_health_label):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 20
        self.label = str(health)
        self.color = (25, 255, 124)
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, self.color)
        self.position = (enemy_health_label.position[0] + 60, enemy_health_label.position[1])

    def update(self, health, enemy_health_label):
        self.label = str(health)

        if health <= 2:
            self.color = (255, 100, 100)

        self.image = self.fontObj.render(self.label, True, self.color)

        self.position = (enemy_health_label.position[0] + 50, enemy_health_label.position[1])

class GameOverLabel:

    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 50
        self.label = "GAME OVER"
        self.color = (255, 100, 100)
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, self.color)
        self.position = (150, 400)

class GameWonLabel:
    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 50
        self.label = "GAME WON"
        self.color = (25, 255, 124)
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, self.color)
        self.position = (150, 400)
