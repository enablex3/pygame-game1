import random
from enemy import Enemy
from enemyBoss1 import EnemyBoss1


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

    def __init__(self, difficulty_setting):
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
                enemies.append(Enemy(enemy_shot_frequency, enemy_velocity))

            self.waves.append(enemies)

            enemies = []

        # add a boss after all waves defeated
        self.waves.append([EnemyBoss1()])

    def get_next_wave(self):
        try:
            self.waves.remove(self.waves[self.current_wave_number])
            return self.waves[self.current_wave_number]
        except:
            return []
            pass
