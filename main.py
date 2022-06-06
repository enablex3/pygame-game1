import threading
import json
import pygame_menu
from wave import Wave
from gametext import *
from player import Player

# init pygame
pygame.init()

# load player settings
SETTINGS_FILE = "settings.json"
with open(SETTINGS_FILE, "r") as settingsJsonFile:
    settings = json.load(settingsJsonFile)

music_enabled_setting = (settings["player_settings"]["music"] == "ON")
sfx_enabled_setting = (settings["player_settings"]["sfx"] == "ON")
difficulty_setting = settings["player_settings"]["difficulty"]
ship = settings["player_settings"]["ship"]

# caption
pygame.display.set_caption("Whacking Space")
pygame.mixer.init()

# game window config
WIDTH, HEIGHT = 500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

# background and mouse settings
BACKGROUND = pygame.image.load("sprites/background.png").convert_alpha()
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

def set_difficulty(value, difficulty):
    global difficulty_setting
    difficulty_setting = value[0][0]

def set_music(value, music_enabled):
    global music_enabled_setting
    music_enabled_setting = value[0][0] == "ON"

def set_sfx(value, sfx_enabled):
    global sfx_enabled_setting
    sfx_enabled_setting = value[0][0] == "ON"

def set_goblin_ship():
    global ship
    ship = settings["options"]["ships"]["goblin"]

def set_blue_ship():
    global ship
    ship = settings["options"]["ships"]["blue_angel"]

def set_red_ship():
    global ship
    ship = settings["options"]["ships"]["dark_red"]

def set_yellow_ship():
    global ship
    ship = settings["options"]["ships"]["yellow_stinger"]


def main():
    # obtain settings
    ships = settings["options"]["ships"]

    music = settings["player_settings"]["music"]
    music_options = settings["options"]["music"]

    sfx = settings["player_settings"]["sfx"]
    sfx_options = settings["options"]["sfx"]

    difficulty = settings["player_settings"]["difficulty"]
    difficulty_options = settings["options"]["difficulty"]

    menu = pygame_menu.Menu('Main Menu', 500, 800, theme=pygame_menu.themes.THEME_DARK)

    menu.add.selector('Difficulty: ', [('EASY', 1), ('MEDIUM', 2), ('HARD', 3)], onchange=set_difficulty).set_value(difficulty_options.index(difficulty))
    menu.add.selector('Music: ', [('ON', 1), ('OFF', 0)], onchange=set_music).set_value(music_options.index(music))
    menu.add.selector('SFX: ', [('ON', 1), ('OFF', 0)], onchange=set_sfx).set_value(sfx_options.index(sfx))

    menu.add.button('Goblin', set_goblin_ship, accept_kwargs=True, font_size=18)
    menu.add.image(ships["goblin"]["original_img"])

    menu.add.button('Blue Angel', set_blue_ship, accept_kwargs=True, font_size=18)
    menu.add.image(ships["blue_angel"]["original_img"])

    menu.add.button('Dark Red', set_red_ship, accept_kwargs=True, font_size=18)
    menu.add.image(ships["dark_red"]["original_img"])

    menu.add.button('Yellow Stinger', set_yellow_ship, accept_kwargs=True, font_size=18)
    menu.add.image(ships["yellow_stinger"]["original_img"])

    menu.add.button('Play', play_game)
    menu.add.button('Quit', pygame_menu.events.PYGAME_QUIT)

    menu.mainloop(WIN)

def draw_game_window(game_over_sound_played,
                     game_won_sound_played,
                     player_health_label,
                     player_health_indicator,
                     enemies_label,
                     enemies_indicator,
                     wave_label,
                     wave_indicator,
                     game_over_label,
                     game_won_label,
                     player,
                     enemies,
                     wave,
                     transition_time,
                     transition_active):

    WIN.blit(BACKGROUND, (0, 0))  # this doesn't actually display yet

    # display labels and indicators
    WIN.blit(player_health_label.image, player_health_label.position)
    WIN.blit(player_health_indicator.image, player_health_indicator.position)
    WIN.blit(enemies_label.image, enemies_label.position)
    WIN.blit(enemies_indicator.image, enemies_indicator.position)

    # if the player is alive, display - else, game over
    if player.health != 0:
        WIN.blit(player.image, (player.rect.x, player.rect.y))
    else:
        WIN.blit(game_over_label.image, game_over_label.position)
        if not game_over_sound_played:
            game_over_sound_played = True
            if music_enabled_setting:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound("sfx/lose.wav"))

    # display player lives
    live_img_spacing = 20
    for k in range(0, player.health):
        WIN.blit(player.lives_img, (live_img_spacing, 20))
        live_img_spacing += 25

    # display each enemy, their bullets and associated explosions
    seconds = (pygame.time.get_ticks() - transition_time) / 1000
    if seconds > 5:
        for enemy in enemies:
            WIN.blit(enemy.image, (enemy.rect.x, enemy.rect.y))

            for bullet in enemy.bullets:
                WIN.blit(bullet.image, (bullet.rect.x, bullet.rect.y))

        # display player bullets
        for bullet in player.bullets:
            WIN.blit(bullet.image, (bullet.rect.x, bullet.rect.y))

        transition_active = False
    else:
        if len(wave.waves) != 0:
            WIN.blit(wave_label.image, wave_label.position)
            WIN.blit(wave_indicator.image, wave_indicator.position)

    # if no enemies left, player won
    if len(wave.waves) == 0:
        WIN.blit(game_won_label.image, game_won_label.position)
        if not game_won_sound_played:
            game_won_sound_played = True
            if music_enabled_setting:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound("sfx/win.wav"))

    pygame.display.update()  # this finally updates the display

    return game_over_sound_played, game_won_sound_played, transition_active


def play_game():
    # save the new settings first
    global settings

    settings["player_settings"]["music"] = "ON" if music_enabled_setting else "OFF"
    settings["player_settings"]["sfx"] = "ON" if sfx_enabled_setting else "OFF"
    settings["player_settings"]["ship"] = ship
    settings["player_settings"]["difficulty"] = difficulty_setting

    with open(SETTINGS_FILE, "w") as settingsJsonFile:
        json.dump(settings, settingsJsonFile)

    # banner for text
    banner = pygame.Rect(0, 0, WIDTH, 60)
    banner_color = (0, 0, 0)

    # load the player
    player = Player(ship)

    # load waves
    wave = Wave(difficulty_setting)
    starting_enemies = wave.waves[wave.current_wave_number]
    enemies = starting_enemies
    wave_number = 1

    # load text
    player_health_label = PlayerHealthLabel()
    player_health_indicator = PlayerHealthIndicator(player.health)
    game_over_label = GameOverLabel()
    game_won_label = GameWonLabel()
    enemies_label = EnemiesLabel()
    enemies_indicator = EnemiesIndicator(enemies)
    wave_label = WavesLabel(WIDTH, HEIGHT)
    wave_indicator = WavesIndicator(wave_number, WIDTH, HEIGHT)

    game_over_sound_played = False
    game_won_sound_played = False

    clock = pygame.time.Clock()

    run = True

    transition_time = pygame.time.get_ticks()
    transition_active = True

    while run:

        clock.tick(FPS)

        events = pygame.event.get()

        pygame.mouse.set_visible(False)

        for event in events:
            if event.type == pygame.QUIT:
                run = False

            # add a new bullet to the player bullet list if condition met
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.add_bullet(sfx_enabled_setting)

        # updates the player based on keys pressed
        player.update(pygame.key.get_pressed())

        # update the enemy
        if not transition_active:
            for enemy in enemies:
                enemy.update()

                if enemy.health == 0:
                    enemies.remove(enemy)
                    if sfx_enabled_setting:
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound("sfx/explosion.wav"))

                enemy.add_bullet(sfx_enabled_setting)
                enemy.shoot()
                enemy.detect_hit(player, sfx_enabled_setting)

            player.shoot()

            for enemy in enemies:
                player.detect_hit(enemy, sfx_enabled_setting)

            player_health_indicator.update(player.health)
            enemies_indicator.update(enemies)

        wave_indicator.update(wave_number)
        pygame.draw.rect(WIN, banner_color, banner)

        game_over_sound_played, game_won_sound_played, transition_active = \
            draw_game_window(game_over_sound_played,
                             game_won_sound_played,
                             player_health_label,
                             player_health_indicator,
                             enemies_label,
                             enemies_indicator,
                             wave_label,
                             wave_indicator,
                             game_over_label,
                             game_won_label,
                             player,
                             enemies,
                             wave,
                             transition_time,
                             transition_active)

        if len(enemies) == 0 and len(wave.waves) != 0:
            enemies = wave.get_next_wave()
            wave_number += 1

            # we want to reset the player's beam overheating values
            player.beam_cooldown_timer = None
            player.beams_overheated = False
            player.bullets_shot = 0

            # give the player back one life
            player.add_health()

            # reset transition time
            transition_time = pygame.time.get_ticks()
            transition_active = True

        # just for accurate wave indicator value
        if len(wave.waves) == 0:
            wave_number = 0

    main()


if __name__ == "__main__":
    main()

"""# set game_loaded
game_loaded = False
loading_image = pygame.image.load("sprites/playerShip.png").convert_alpha()
loading_image = pygame.transform.scale(loading_image, (200, 200))
loading_label = LoadingLabel()

# load screen function
def display_loading_screen():
    clock = pygame.time.Clock()
    start_load_time = pygame.time.get_ticks()
    load_sound_played = False
    while True:
        clock.tick(FPS)

        WIN.fill((255, 255, 255))
        WIN.blit(loading_image, (150, 300))
        WIN.blit(loading_label.image, loading_label.position)

        pygame.display.update()

        global game_loaded
        global music_enabled_setting

        if not load_sound_played:
            load_sound_played = True
            if music_enabled_setting:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("sfx/load.wav"))

        if game_loaded:
            break

# starting the loading thread
loading_thread = threading.Thread(target=display_loading_screen)
loading_thread.start()"""

"""# stop loading thread
game_loaded = True
loading_thread.join()"""
