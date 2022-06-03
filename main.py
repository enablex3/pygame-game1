import threading
import json
from wave import Wave
from gametext import *
from player import Player

# load player settings
with open("settings.json", "r") as settingsJsonFile:
    settings = json.load(settingsJsonFile)

music_enabled_setting = (settings["player_settings"]["music_enabled"] == "true")
sfx_enabled_setting = (settings["player_settings"]["sfx_enabled"] == "true")

# caption
pygame.display.set_caption("Whacking Space")
pygame.mixer.init()

# game window config
WIDTH, HEIGHT = 500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

# set game_loaded
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
            seconds = (pygame.time.get_ticks() - start_load_time) / 1000
            if seconds > 3:
                break

# starting the loading thread
loading_thread = threading.Thread(target=display_loading_screen)
loading_thread.start()

# background and mouse settings
BACKGROUND = pygame.image.load("sprites/background.png").convert_alpha()
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

# banner for text
banner = pygame.Rect(0, 0, WIDTH, 60)
banner_color = (0, 0, 0)

# load the player
player = Player()

# load waves
wave = Wave()
starting_enemies = wave.waves[wave.current_wave_number]
enemies = starting_enemies
wave_number = 1

# load text
ammo_label = AmmoLabel()
ammo_indicator = AmmoIndicator()
player_health_label = PlayerHealthLabel()
player_health_indicator = PlayerHealthIndicator(player.health)
game_over_label = GameOverLabel()
game_won_label = GameWonLabel()
enemies_label = EnemiesLabel()
enemies_indicator = EnemiesIndicator(enemies)
wave_label = WavesLabel()
wave_indicator = WavesIndicator(wave_number)

# menu text
menu_label = MenuLabel()
music_label = MusicLabel()
music_enabled = MusicEnable()
music_disable = MusicDisable()
sfx_label = SFXLabel()
sfx_enabled = SFXEnable()
sfx_disable = SFXDisable()

# stop loading thread
game_loaded = True
loading_thread.join()

game_over_sound_played = False
game_won_sound_played = False

show_menu = True

def draw_menu():
    WIN.fill((255, 255, 255))
    WIN.blit(menu_label.image, menu_label.position)
    WIN.blit(music_label.image, music_label.position)
    WIN.blit(music_enabled.image, music_enabled.position)
    WIN.blit(music_disable.image, music_disable.position)
    WIN.blit(sfx_label.image, sfx_label.position)
    WIN.blit(sfx_enabled.image, sfx_enabled.position)
    WIN.blit(sfx_disable.image, sfx_disable.position)

    pygame.display.update()


def draw_game_window():
    global game_over_sound_played
    global game_won_sound_played

    WIN.blit(BACKGROUND, (0, 0))  # this doesn't actually display yet
    pygame.draw.rect(WIN, banner_color, banner)

    # display labels and indicators
    WIN.blit(ammo_label.image, ammo_label.position)
    WIN.blit(ammo_indicator.image, ammo_indicator.position)
    WIN.blit(player_health_label.image, player_health_label.position)
    WIN.blit(player_health_indicator.image, player_health_indicator.position)
    WIN.blit(enemies_label.image, enemies_label.position)
    WIN.blit(enemies_indicator.image, enemies_indicator.position)
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

    # display each enemy, their bullets and associated explosions
    for enemy in enemies:
        WIN.blit(enemy.image, (enemy.rect.x, enemy.rect.y))
        WIN.blit(enemy.health_label.image, enemy.health_label.position)
        WIN.blit(enemy.health_indicator.image, enemy.health_indicator.position)

        for bullet in enemy.bullets:
            WIN.blit(bullet.image, (bullet.rect.x, bullet.rect.y))

    # if no enemies left, player won
    if len(wave.waves) == 0:
        WIN.blit(game_won_label.image, game_won_label.position)
        if not game_won_sound_played:
            game_won_sound_played = True
            if music_enabled_setting:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound("sfx/win.wav"))

    # display player bullets
    for bullet in player.bullets:
        WIN.blit(bullet.image, (bullet.rect.x, bullet.rect.y))

    pygame.display.update()  # this finally updates the display

def main():
    global enemies
    global wave_number
    global sfx_enabled_setting
    global show_menu

    clock = pygame.time.Clock()

    run = True

    while run:

        clock.tick(FPS)

        events = pygame.event.get()

        if not show_menu:

            pygame.mouse.set_visible(False)

            for event in events:
                if event.type == pygame.QUIT:
                    run = False

                # add a new bullet to the player bullet list if condition met
                if not "RELOAD" in ammo_indicator.label:
                    update_ammo_text = player.add_bullet(pygame.key.get_pressed(), sfx_enabled_setting)

                if update_ammo_text:
                    ammo_indicator.update()

            # updates the player based on keys pressed
            player.update(pygame.key.get_pressed())

            # update the enemy
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

            ammo_indicator.reload(pygame.key.get_pressed())
            player_health_indicator.update(player.health)
            enemies_indicator.update(enemies)
            wave_indicator.update(wave_number)

            draw_game_window()

            if len(enemies) == 0:
                enemies = wave.get_next_wave()
                wave_number += 1

            # just for accurate wave indicator value
            if len(wave.waves) == 0:
                wave_number = 0

        else:
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                if pygame.key.get_pressed()[pygame.K_q]:
                    show_menu = False

            draw_menu()

    pygame.quit()


if __name__ == "__main__":
    main()
