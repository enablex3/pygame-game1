import os
import json
import random
import pygame_menu

from wave.wave import Wave
from gametext import *
from player.player import Player
from star_field import StarField
from asteroid.asteroid import Asteroid
from player.cannonindicator import CannonIndicator

os.environ["SDL_VIDEO_CENTERED"] = '1'

# init pygame
pygame.init()

# display information from system to get width and height
info = pygame.display.Info()
window_width, window_height = info.current_w, info.current_h

# load player settings
SETTINGS_FILE = "settings.json"
with open(SETTINGS_FILE, "r") as settingsJsonFile:
    settings = json.load(settingsJsonFile)

music_enabled_setting = (settings["player_settings"]["music"] == "ON")
sfx_enabled_setting = (settings["player_settings"]["sfx"] == "ON")
difficulty_setting = settings["player_settings"]["difficulty"]
ship = settings["player_settings"]["ship"]
highscore = int(settings["player_settings"]["highscore"])

# caption
pygame.display.set_caption("Whacking Space")
pygame.mixer.init()

# game window config
WIN = pygame.display.set_mode((window_width, window_height))
FPS = 60

star_field = StarField(window_width, window_height)

beam_cool_down = CannonIndicator(window_width)

cooldown_rate = 0.25 # 0.25 second to cool down
HEAT_RATE = 10 # to take 10 away from cool_down_amount
COOLDOWN_MAX_AMOUNT = 100

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

    menu = pygame_menu.Menu('Main Menu', window_width, window_height, theme=pygame_menu.themes.THEME_DARK)

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

def determine_cool_down(cool_down_time, cool_down_amount, overheated):
    global cooldown_rate

    cool_down_indicator = 1

    if cool_down_amount == 0:
        overheated = True
        cooldown_rate = 0.5

    elif cool_down_amount >= 30:
        overheated = False
        cooldown_rate = 0.25

    if not cool_down_time is None:
        seconds = (pygame.time.get_ticks() - cool_down_time) / 1000

        if seconds >= cooldown_rate:
            cool_down_amount += HEAT_RATE
            cool_down_time = None

    if cool_down_time is None and cool_down_amount != COOLDOWN_MAX_AMOUNT:
        cool_down_time = pygame.time.get_ticks()

    cool_down_indicator = cool_down_amount / COOLDOWN_MAX_AMOUNT

    return cool_down_indicator, cool_down_amount, cool_down_time, overheated

def draw_star_field():
    WIN.fill(star_field.COLORS[3])
    # animate some motherfucking stars
    for star in star_field.star_field_slow:
        star[1] += 1
        if star[1] > window_height:
            star[0] = random.randrange(0, window_width)
            star[1] = random.randrange(-20, -5)
        pygame.draw.circle(WIN, star_field.COLORS[2], star, 3)

    for star in star_field.star_field_medium:
        star[1] += 4
        if star[1] > window_height:
            star[0] = random.randrange(0, window_width)
            star[1] = random.randrange(-20, -5)
        pygame.draw.circle(WIN, star_field.COLORS[6], star, 2)

def draw_game_window(game_over_sound_played,
                     game_won_sound_played,
                     highscore_label,
                     highscore_indicator,
                     wave_label,
                     wave_indicator,
                     game_over_label,
                     game_won_label,
                     player,
                     enemies,
                     wave,
                     transition_time,
                     transition_active,
                     asteroid,
                     beam_cool_down):

    # display labels and indicators
    WIN.blit(highscore_label.image, highscore_label.position)
    WIN.blit(highscore_indicator.image, highscore_indicator.position)

    # display each enemy, their bullets and associated explosions
    seconds = (pygame.time.get_ticks() - transition_time) / 1000
    if seconds > 3:
        for enemy in enemies:
            WIN.blit(enemy.image, (enemy.rect.x, enemy.rect.y))

            for bullet in enemy.bullets:
                WIN.blit(bullet.image, (bullet.rect.x, bullet.rect.y))

        # display player bullets
        for bullet in player.bullets:
            WIN.blit(bullet.image, (bullet.rect.x, bullet.rect.y))

        # display player missiles
        for missile in player.missiles:
            WIN.blit(missile.img, (missile.rect.x, missile.rect.y))

        transition_active = False
    else:
        if len(wave.waves) != 0:
            WIN.blit(wave_label.image, wave_label.position)
            WIN.blit(wave_indicator.image, wave_indicator.position)

    # if the player is alive, display - else, game over
    if player.health != 0:
        WIN.blit(player.image, (player.rect.x, player.rect.y))
    else:
        WIN.blit(game_over_label.image, game_over_label.position)
        if not game_over_sound_played:
            game_over_sound_played = True
            if music_enabled_setting:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound("sfx/lose.wav"))

    # player force field if condition met
    if player.force_field_show:
        WIN.blit(player.force_field.img, (player.force_field.rect.x, player.force_field.rect.y))

    # display player lives
    live_img_spacing = window_width // 4
    for k in range(0, player.health):
        WIN.blit(player.lives_img, (live_img_spacing, 20))
        live_img_spacing += 25

    # display cool down indicator
    WIN.blit(beam_cool_down.img, beam_cool_down.position)

    # if no enemies left, player won
    if len(wave.waves) == 0:
        WIN.blit(game_won_label.image, game_won_label.position)
        if not game_won_sound_played:
            game_won_sound_played = True
            if music_enabled_setting:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound("sfx/win.wav"))

    if not asteroid is None:
        WIN.blit(asteroid.image, (asteroid.rect.x, asteroid.rect.y))

    pygame.display.update()  # this finally updates the display

    return game_over_sound_played, game_won_sound_played, transition_active


def play_game():
    # save the new settings first
    global settings
    global highscore

    settings["player_settings"]["music"] = "ON" if music_enabled_setting else "OFF"
    settings["player_settings"]["sfx"] = "ON" if sfx_enabled_setting else "OFF"
    settings["player_settings"]["ship"] = ship
    settings["player_settings"]["difficulty"] = difficulty_setting

    with open(SETTINGS_FILE, "w") as settingsJsonFile:
        json.dump(settings, settingsJsonFile, indent=4)

    # banner for text
    banner = pygame.Rect(0, 0, window_width, 60)
    banner_color = (0, 0, 0)

    # load the player
    player = Player(ship, window_width, window_height)

    # load waves
    wave = Wave(difficulty_setting, window_width, window_height)
    starting_enemies = wave.waves[wave.current_wave_number]
    enemies = starting_enemies
    wave_number = 1

    # load text
    game_over_label = GameOverLabel(window_width, window_height)
    game_won_label = GameWonLabel(window_width, window_height)
    highscore_label = HighScoreLabel(window_width)
    highscore_indicator = HighScoreIndicator(highscore, window_width)
    wave_label = WavesLabel(window_width, window_height)
    wave_indicator = WavesIndicator(wave_number, window_width, window_height)

    game_over_sound_played = False
    game_won_sound_played = False

    clock = pygame.time.Clock()

    run = True

    transition_time = pygame.time.get_ticks()
    transition_active = True

    score = 0

    asteroid = None

    cool_down_amount = COOLDOWN_MAX_AMOUNT
    cool_down_time = None
    cool_down_indicator = 1
    overheated = False

    while run:

        clock.tick(FPS)

        events = pygame.event.get()

        pygame.mouse.set_visible(False)

        for event in events:
            if event.type == pygame.QUIT:
                run = False

            # add a new bullet to the player bullet list if condition met
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not overheated:
                    player.add_bullet(sfx_enabled_setting)
                    cool_down_time = pygame.time.get_ticks()
                    cool_down_amount -= HEAT_RATE
                if event.button == 3:
                    player.add_missile()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    player.show_force_field()

            if event.type == pygame.KEYUP:
                player.image = player.original_img

        cool_down_indicator, cool_down_amount, cool_down_time, overheated = \
            determine_cool_down(cool_down_time, cool_down_amount, overheated)

        beam_cool_down.update(cool_down_indicator)

        # updates the player based on keys pressed
        player.update(pygame.key.get_pressed())

        # update the enemy
        if not transition_active:
            for enemy in enemies:
                enemy.update()

                if enemy.health <= 0:
                    enemies.remove(enemy)
                    if sfx_enabled_setting:
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound("sfx/explosion.wav"))
                    score += 1

                enemy.add_bullet(sfx_enabled_setting)
                enemy.shoot()
                enemy.detect_hit(player, sfx_enabled_setting)

            player.shoot()
            player.shoot_missile()

            for enemy in enemies:
                player.detect_hit(enemy, sfx_enabled_setting)

            if score > highscore:
                highscore_indicator.update(score)
                highscore = score

        wave_indicator.update(wave_number)
        pygame.draw.rect(WIN, banner_color, banner)

        draw_star_field()

        if wave_number % 2 == 0:
            # spawn asteroid
            if asteroid is None and not transition_active:
                asteroid = Asteroid()
            elif not transition_active:
                asteroid.update()

                if asteroid.rect.x == 0 or asteroid.rect.x == 500:
                    # init new asteroid if the current one goes out of bounds
                    asteroid = Asteroid()

                astroid_hit = False

                for beam in player.bullets:
                    if beam.rect.colliderect(asteroid.rect):
                        astroid_hit = True
                        break

                if astroid_hit:
                    if asteroid.material == "COOLANT":
                        # we want to reset the player's beam overheating values
                        cool_down_amount = 100
                        cool_down_time = None
                        cool_down_indicator = 1

                    elif asteroid.material == "LIFE":
                        player.add_life()

                    asteroid = None

        else:
            asteroid = None


        game_over_sound_played, game_won_sound_played, transition_active = \
            draw_game_window(game_over_sound_played,
                             game_won_sound_played,
                             highscore_label,
                             highscore_indicator,
                             wave_label,
                             wave_indicator,
                             game_over_label,
                             game_won_label,
                             player,
                             enemies,
                             wave,
                             transition_time,
                             transition_active,
                             asteroid,
                             beam_cool_down)

        if len(enemies) == 0 and len(wave.waves) != 0:
            enemies = wave.get_next_wave()
            wave_number += 1

            # we want to reset the player's beam overheating values
            player.beam_cooldown_timer = None
            player.beams_overheated = False
            player.bullets_shot = 0

            # give the player back one life
            player.add_life()

            # reset transition time
            transition_time = pygame.time.get_ticks()
            transition_active = True

        # just for accurate wave indicator value
        if len(wave.waves) == 0:
            wave_number = 0

        if transition_active:
            # remove bullets from player and enemies
            for enemy in enemies:
                enemy.bullets = []

            player.bullets = []

    settings["player_settings"]["highscore"] = highscore

    with open(SETTINGS_FILE, "w") as settingsJsonFile:
        json.dump(settings, settingsJsonFile, indent=4)

    main()


if __name__ == "__main__":
    main()
