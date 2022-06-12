import random
from enemy.blazer import Blazer
from enemy.apache import Apache


def determine_wave_attributes(difficulty_setting):
    # init values with 'easy' setting
    enemy_shot_frequency = 6
    enemy_velocity = 3
    waves = 3

    if difficulty_setting == "MEDIUM":
        enemy_shot_frequency = 5
        enemy_velocity = 6
        waves = 4

    elif difficulty_setting == "HARD":
        enemy_shot_frequency = 3
        enemy_velocity = 8
        waves = 5

    return enemy_shot_frequency, enemy_velocity, waves


class Wave:

    def __init__(self, difficulty_setting, window_width, window_height):
        self.waves = []
        self.current_wave_number = 0

        # difficulty dictates number of waves, enemy speed, and enemy shot frequency
        enemy_shot_frequency, enemy_velocity, waves = determine_wave_attributes(difficulty_setting)

        # fixed value for number of waves (for now)
        enemies = []
        starting_enemy_amount_lower = 1
        starting_enemy_amount_higher = 3

        for k in range(0, waves):
            enemy_amount = random.randrange(starting_enemy_amount_lower, starting_enemy_amount_higher)

            starting_enemy_amount_lower = starting_enemy_amount_higher
            starting_enemy_amount_higher = starting_enemy_amount_higher + 2

            for i in range(0, enemy_amount):
                enemies.append(Blazer(enemy_shot_frequency, enemy_velocity, window_width, window_height))

            self.waves.append(enemies)

            enemies = []

        # add a boss after all waves defeated
        final_wave = [Blazer(enemy_shot_frequency, enemy_velocity, window_width, window_height) for enemy in range(0, starting_enemy_amount_higher - 2)]
        final_wave.append(Apache())
        self.waves.append(final_wave)

    def get_next_wave(self):
        try:
            self.waves.remove(self.waves[self.current_wave_number])
            return self.waves[self.current_wave_number]
        except:
            return []
            pass
