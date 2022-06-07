import pygame

pygame.font.init()

LABEL_X = 120
LABEL_Y = 20
INDICATOR_X = LABEL_X + 50

class LoadingLabel:

    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 50
        self.label = "Loading..."
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (0, 0, 0))
        self.position = (175, 500)

class HighScoreLabel:
    def __init__(self):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 30
        self.label = "HIGHSCORE"
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (255, 255, 255))
        self.position = (LABEL_X + 50, LABEL_Y - 20)


class HighScoreIndicator:

    def __init__(self, score):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 20
        self.label = str(score)
        self.color = (255, 255, 255)
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, self.color)
        self.position = (LABEL_X + 100, LABEL_Y + 10)

    def update(self, score):
        self.label = str(score)

        self.image = self.fontObj.render(self.label, True, self.color)

class WavesLabel:
    def __init__(self, WIN_WIDTH, WIN_HEIGHT):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 50
        self.label = "Wave"
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, (255, 255, 255))
        self.position = ((WIN_WIDTH // 2) - 60, WIN_HEIGHT // 2)


class WavesIndicator:

    def __init__(self, wave_number, WIN_WIDTH, WIN_HEIGHT):
        self.font = pygame.font.get_default_font() + ".ttf"
        self.size = 50
        self.label = str(wave_number)
        self.color = (255, 255, 255)
        self.fontObj = pygame.font.SysFont(self.font, self.size)
        self.image = self.fontObj.render(self.label, True, self.color)
        self.position = ((WIN_WIDTH // 2) + 40, WIN_HEIGHT // 2)

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
