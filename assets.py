# Asset Manager for Stone Age Agents
import pygame

class AssetManager:
    def __init__(self):
        self.scout_sprite = None
        self.gatherer_sprite = None
        self.tribe_sprite = None
        self.food_sprite = None
        self.wood_sprite = None
        self.stone_sprite = None
        self.health_sprite = None
        self.happy_sprite = None
        self.population_sprite = None
        self.food_sprite_small = None
        self.wood_sprite_small = None
        self.stone_sprite_small = None
        self.health_sprite_small = None
        self.happy_sprite_small = None
        self.population_sprite_small = None

    def load_assets(self):
        # Load and prepare sprites
        self.scout_sprite = pygame.image.load('assets/scout.png').convert_alpha()
        self.scout_sprite.set_colorkey((255, 255, 255))
        self.scout_sprite = pygame.transform.scale(self.scout_sprite, (40, 40))

        self.gatherer_sprite = pygame.image.load('assets/gatherer.png').convert_alpha()
        self.gatherer_sprite = pygame.transform.scale(self.gatherer_sprite, (40, 40))

        self.tribe_sprite = pygame.image.load('assets/tribe.png').convert_alpha()
        self.tribe_sprite.set_colorkey((255, 255, 255))
        self.tribe_sprite = pygame.transform.scale(self.tribe_sprite, (48, 48))

        # Resource sprites for overlay (regular size)
        self.food_sprite = pygame.image.load('assets/food.png').convert_alpha()
        original_width, original_height = self.food_sprite.get_size()
        scale_factor = 30 / original_height
        new_width = int(original_width * scale_factor)
        self.food_sprite = pygame.transform.scale(self.food_sprite, (new_width, 30))

        self.wood_sprite = pygame.image.load('assets/wood.png').convert_alpha()
        original_width, original_height = self.wood_sprite.get_size()
        scale_factor = 30 / original_height
        new_width = int(original_width * scale_factor)
        self.wood_sprite = pygame.transform.scale(self.wood_sprite, (new_width, 30))

        self.stone_sprite = pygame.image.load('assets/stone.png').convert_alpha()
        original_width, original_height = self.stone_sprite.get_size()
        scale_factor = 30 / original_height
        new_width = int(original_width * scale_factor)
        self.stone_sprite = pygame.transform.scale(self.stone_sprite, (new_width, 30))

        # Health sprite for overlay
        self.health_sprite = pygame.image.load('assets/health.png').convert_alpha()
        original_width, original_height = self.health_sprite.get_size()
        scale_factor = 30 / original_height
        new_width = int(original_width * scale_factor)
        self.health_sprite = pygame.transform.scale(self.health_sprite, (new_width, 30))

        # Happy sprite for overlay
        self.happy_sprite = pygame.image.load('assets/happy.png').convert_alpha()
        original_width, original_height = self.happy_sprite.get_size()
        scale_factor = 30 / original_height
        new_width = int(original_width * scale_factor)
        self.happy_sprite = pygame.transform.scale(self.happy_sprite, (new_width, 30))

        # Population sprite for overlay
        self.population_sprite = pygame.image.load('assets/population.png').convert_alpha()
        original_width, original_height = self.population_sprite.get_size()
        scale_factor = 30 / original_height
        new_width = int(original_width * scale_factor)
        self.population_sprite = pygame.transform.scale(self.population_sprite, (new_width, 30))

        # Small resource sprites for tribe info bar (25% smaller)
        small_height = 23  # 30 * 0.75, rounded up
        self.food_sprite_small = pygame.image.load('assets/food.png').convert_alpha()
        original_width, original_height = self.food_sprite_small.get_size()
        scale_factor = small_height / original_height
        new_width = int(original_width * scale_factor)
        self.food_sprite_small = pygame.transform.scale(self.food_sprite_small, (new_width, small_height))

        self.wood_sprite_small = pygame.image.load('assets/wood.png').convert_alpha()
        original_width, original_height = self.wood_sprite_small.get_size()
        scale_factor = small_height / original_height
        new_width = int(original_width * scale_factor)
        self.wood_sprite_small = pygame.transform.scale(self.wood_sprite_small, (new_width, small_height))

        self.stone_sprite_small = pygame.image.load('assets/stone.png').convert_alpha()
        original_width, original_height = self.stone_sprite_small.get_size()
        scale_factor = small_height / original_height
        new_width = int(original_width * scale_factor)
        self.stone_sprite_small = pygame.transform.scale(self.stone_sprite_small, (new_width, small_height))

        # Small health sprite for tribe info bar
        self.health_sprite_small = pygame.image.load('assets/health.png').convert_alpha()
        original_width, original_height = self.health_sprite_small.get_size()
        scale_factor = small_height / original_height
        new_width = int(original_width * scale_factor)
        self.health_sprite_small = pygame.transform.scale(self.health_sprite_small, (new_width, small_height))

        # Small happy sprite for tribe info bar
        self.happy_sprite_small = pygame.image.load('assets/happy.png').convert_alpha()
        original_width, original_height = self.happy_sprite_small.get_size()
        scale_factor = small_height / original_height
        new_width = int(original_width * scale_factor)
        self.happy_sprite_small = pygame.transform.scale(self.happy_sprite_small, (new_width, small_height))

        # Small population sprite for tribe info bar
        self.population_sprite_small = pygame.image.load('assets/population.png').convert_alpha()
        original_width, original_height = self.population_sprite_small.get_size()
        scale_factor = small_height / original_height
        new_width = int(original_width * scale_factor)
        self.population_sprite_small = pygame.transform.scale(self.population_sprite_small, (new_width, small_height))

    def draw_scout(self, screen, x, y):
        screen.blit(self.scout_sprite, (x, y))

    def draw_gatherer(self, screen, x, y):
        screen.blit(self.gatherer_sprite, (x, y))

    def draw_tribe(self, screen, x, y):
        screen.blit(self.tribe_sprite, (x, y))

    def draw_food(self, screen, x, y):
        screen.blit(self.food_sprite, (x, y))

    def draw_wood(self, screen, x, y):
        screen.blit(self.wood_sprite, (x, y))

    def draw_stone(self, screen, x, y):
        screen.blit(self.stone_sprite, (x, y))

    def draw_health(self, screen, x, y):
        screen.blit(self.health_sprite, (x, y))

    def draw_happy(self, screen, x, y):
        screen.blit(self.happy_sprite, (x, y))

    def draw_population(self, screen, x, y):
        screen.blit(self.population_sprite, (x, y))

    def draw_food_small(self, screen, x, y):
        screen.blit(self.food_sprite_small, (x, y))

    def draw_wood_small(self, screen, x, y):
        screen.blit(self.wood_sprite_small, (x, y))

    def draw_stone_small(self, screen, x, y):
        screen.blit(self.stone_sprite_small, (x, y))

    def draw_health_small(self, screen, x, y):
        screen.blit(self.health_sprite_small, (x, y))

    def draw_happy_small(self, screen, x, y):
        screen.blit(self.happy_sprite_small, (x, y))

    def draw_population_small(self, screen, x, y):
        screen.blit(self.population_sprite_small, (x, y))