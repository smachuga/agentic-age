
import numpy as np
import random
from noise import pnoise2

class World:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.terrain_types = ['grassland', 'forest', 'river', 'ridge', 'savanna', 'mountain']
        self.map = self.generate_map()
        self.resources = self.spawn_resources()
        self.explored = np.zeros((self.height, self.width), dtype=bool)  # False = unexplored, True = explored
        self.day = 0
        self.weather = "clear"

    def generate_map(self):
        # Perlin noise parameters (tuned for more variety)
        scale = 8.0
        octaves = 4
        persistence = 0.5
        lacunarity = 2.0
        seed = random.randint(0, 100)

        terrain_map = np.empty((self.height, self.width), dtype=object)
        for x in range(self.height):
            for y in range(self.width):
                nx = x / self.height
                ny = y / self.width
                noise_val = pnoise2(nx * scale, ny * scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=self.width, repeaty=self.height, base=seed)
                # Assign terrain based on noise value (adjusted thresholds)
                if noise_val < -0.2:
                    terrain = 'river'
                elif noise_val < 0.05:
                    terrain = 'grassland'
                elif noise_val < 0.18:
                    terrain = 'forest'
                elif noise_val < 0.32:
                    terrain = 'savanna'
                elif noise_val < 0.5:
                    terrain = 'ridge'
                else:
                    terrain = 'mountain'
                terrain_map[x, y] = terrain
        return terrain_map

    def spawn_resources(self):
        resources = {}
        for x in range(self.height):
            for y in range(self.width):
                terrain = self.map[x, y]
                resources[(x, y)] = {
                    'food': self.get_food_yield(terrain),
                    'wood': self.get_wood_yield(terrain),
                    'stone': self.get_stone_yield(terrain)
                }
        return resources

    def get_food_yield(self, terrain):
        yields = {
            'grassland': random.randint(4, 10),
            'forest': random.randint(1, 3),
            'river': random.randint(5, 10),
            'savanna': random.randint(6, 12),
            'mountain': 0,
            'ridge': random.randint(0, 1)
        }
        return yields.get(terrain, 0)

    def get_wood_yield(self, terrain):
        yields = {
            'grassland': random.randint(1, 3),
            'forest': random.randint(6, 12),
            'river': 0,
            'savanna': 0,
            'mountain': random.randint(2, 5),
            'ridge': random.randint(0, 1)
        }
        return yields.get(terrain, 0)

    def get_stone_yield(self, terrain):
        yields = {
            'grassland': 0,
            'forest': 0,
            'river': random.randint(1, 3),
            'savanna': 0,
            'mountain': random.randint(4, 10),
            'ridge': random.randint(6, 12)
        }
        return yields.get(terrain, 0)

    def deplete_resources(self, location, resource_type, amount):
        if location in self.resources:
            self.resources[location][resource_type] = max(0, self.resources[location][resource_type] - amount)

    def simulate_day(self):
        self.day += 1
        self.weather = random.choice(["clear", "rain", "storm"])
        weather_modifiers = {'clear': 1.0, 'rain': 1.2, 'storm': 0.5}
        modifier = weather_modifiers.get(self.weather, 1.0)
        for loc in self.resources:
            self.resources[loc]['food'] = max(0, int(self.resources[loc]['food'] * modifier - random.randint(0, 2)))
        return self.trigger_event()

    def trigger_event(self):
        events = [None, {"type": "predator", "effect": "reduce_population", "value": random.randint(1, 3)}]
        return random.choice(events)

    def display_map(self, tribe):
        symbols = {'grassland': 'G', 'forest': 'F', 'river': 'R', 'ridge': 'D', 'savanna': 'S', 'mountain': 'M'}
        for x in range(self.height):
            row = []
            for y in range(self.width):
                if (x, y) == tribe.location:
                    row.append('T')  # Tribe/Chieftain location
                elif any(agent.current_pos == (x, y) for agent in tribe.agents if hasattr(agent, 'current_pos')):
                    row.append('S')  # Scout location
                else:
                    row.append(symbols[self.map[x, y]])
            print(' '.join(row))
        print()