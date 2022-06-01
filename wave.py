import random
from enemy import Enemy

class Wave:

    def __init__(self):
        self.waves = []
        self.current_wave_number = 0

        # fixed value for number of waves (for now)
        enemies = []
        starting_enemy_amount_lower = 1
        starting_enemy_amount_higher = 3

        for k in range(0, 4):
            enemy_amount = random.randrange(starting_enemy_amount_lower, starting_enemy_amount_higher)

            starting_enemy_amount_lower = starting_enemy_amount_higher
            starting_enemy_amount_higher = starting_enemy_amount_higher + 2

            for i in range(0, enemy_amount):
                enemies.append(Enemy())

            self.waves.append(enemies)

            enemies = []

    def get_next_wave(self):
        try:
            self.waves.remove(self.waves[self.current_wave_number])
            return self.waves[self.current_wave_number]
        except:
            return []
            pass
