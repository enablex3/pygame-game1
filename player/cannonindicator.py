import pygame

SIZE = (160, 80)

class CannonIndicator:

    def __init__(self, window_width):
        self.zero_percent_img = pygame.image.load("sprites/player/cannon_indicator/Cannon0Percent.png")
        self.zero_percent_img = pygame.transform.scale(self.zero_percent_img, SIZE)

        self.ten_percent_img = pygame.image.load("sprites/player/cannon_indicator/Cannon10Percent.png")
        self.ten_percent_img = pygame.transform.scale(self.ten_percent_img, SIZE)

        self.twenty_percent_img = pygame.image.load("sprites/player/cannon_indicator/Cannon20Percent.png")
        self.twenty_percent_img = pygame.transform.scale(self.twenty_percent_img, SIZE)

        self.thirty_percent_img = pygame.image.load("sprites/player/cannon_indicator/Cannon30Percent.png")
        self.thirty_percent_img = pygame.transform.scale(self.thirty_percent_img, SIZE)

        self.forty_percent_img = pygame.image.load("sprites/player/cannon_indicator/Cannon40Percent.png")
        self.forty_percent_img = pygame.transform.scale(self.forty_percent_img, SIZE)

        self.fifty_percent_img = pygame.image.load("sprites/player/cannon_indicator/Cannon50Percent.png")
        self.fifty_percent_img = pygame.transform.scale(self.fifty_percent_img, SIZE)

        self.sixty_percent_img = pygame.image.load("sprites/player/cannon_indicator/Cannon60Percent.png")
        self.sixty_percent_img = pygame.transform.scale(self.sixty_percent_img, SIZE)

        self.seventy_percent_img = pygame.image.load("sprites/player/cannon_indicator/Cannon70Percent.png")
        self.seventy_percent_img = pygame.transform.scale(self.seventy_percent_img, SIZE)

        self.eighty_percent_img = pygame.image.load("sprites/player/cannon_indicator/Cannon80Percent.png")
        self.eighty_percent_img = pygame.transform.scale(self.eighty_percent_img, SIZE)

        self.ninety_percent_img = pygame.image.load("sprites/player/cannon_indicator/Cannon90Percent.png")
        self.ninety_percent_img = pygame.transform.scale(self.ninety_percent_img, SIZE)

        self.hundred_percent_img = pygame.image.load("sprites/player/cannon_indicator/Cannon100Percent.png")
        self.hundred_percent_img = pygame.transform.scale(self.hundred_percent_img, SIZE)

        # upon initialization, the img will be the 100% image
        self.img = self.hundred_percent_img

        self.position = (window_width // 2 + SIZE[0], -10)

    def update(self, cooling):

        if cooling == 1:
            self.img = self.hundred_percent_img

        elif cooling == 0.9:
            self.img = self.ninety_percent_img

        elif cooling == 0.8:
            self.img = self.eighty_percent_img

        elif cooling == 0.7:
            self.img = self.seventy_percent_img

        elif cooling == 0.6:
            self.img = self.sixty_percent_img

        elif cooling == 0.5:
            self.img = self.fifty_percent_img

        elif cooling == 0.4:
            self.img = self.forty_percent_img

        elif cooling == 0.3:
            self.img = self.thirty_percent_img

        elif cooling == 0.2:
            self.img = self.twenty_percent_img

        elif cooling == 0.1:
            self.img = self.ten_percent_img

        elif cooling == 0:
            self.img = self.zero_percent_img


