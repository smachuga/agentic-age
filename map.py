# Map module for Stone Age Agents
import pygame
from scout import Scout
from gatherer import Gatherer

CELL_SIZE = 72
MAP_WIDTH = 13  # Number of columns (tiles)
MAP_HEIGHT = 10  # Number of rows (tiles)
WINDOW_WIDTH = CELL_SIZE * MAP_WIDTH
WINDOW_HEIGHT = CELL_SIZE * MAP_HEIGHT + 240  # More space for status and feedback

terrain_colors = {'grassland': (50, 205, 50), 'forest': (34, 139, 34), 'river': (70, 130, 180), 'ridge': (160, 82, 45), 'savanna': (218, 165, 32), 'mountain': (105, 105, 105), 'tribe': (255, 215, 0)}

def draw_map(screen, world, tribe, map_font, asset_manager):
    font = pygame.font.SysFont(None, CELL_SIZE)
    for x in range(world.height):
        for y in range(world.width):
            rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if not world.explored[x, y]:
                pygame.draw.rect(screen, (40, 40, 40), rect)  # Unexplored: dark gray
            else:
                color = terrain_colors[world.map[x, y]]
                pygame.draw.rect(screen, color, rect)
                
                # Add terrain-specific details
                terrain = world.map[x, y]
                if terrain == 'forest':
                    # Draw small trees
                    pygame.draw.circle(screen, (0, 80, 0), (y * CELL_SIZE + 16, x * CELL_SIZE + 16), 8)
                    pygame.draw.circle(screen, (0, 80, 0), (y * CELL_SIZE + 48, x * CELL_SIZE + 24), 8)
                    pygame.draw.circle(screen, (0, 80, 0), (y * CELL_SIZE + 32, x * CELL_SIZE + 48), 8)
                elif terrain == 'river':
                    # Draw wavy lines
                    pygame.draw.line(screen, (100, 149, 237), (y * CELL_SIZE + 8, x * CELL_SIZE + 32), (y * CELL_SIZE + 24, x * CELL_SIZE + 24), 4)
                    pygame.draw.line(screen, (100, 149, 237), (y * CELL_SIZE + 32, x * CELL_SIZE + 40), (y * CELL_SIZE + 48, x * CELL_SIZE + 32), 4)
                elif terrain == 'mountain':
                    # Draw rocky pattern
                    pygame.draw.polygon(screen, (80, 80, 80), [(y * CELL_SIZE + 16, x * CELL_SIZE + 56), (y * CELL_SIZE + 32, x * CELL_SIZE + 16), (y * CELL_SIZE + 48, x * CELL_SIZE + 56)])
                elif terrain == 'grassland':
                    # Add grassland texture
                    for i in range(3):
                        pygame.draw.line(screen, (34, 139, 34), (y * CELL_SIZE + i*20 + 8, x * CELL_SIZE + 56), (y * CELL_SIZE + i*20 + 16, x * CELL_SIZE + 40), 4)
                
                if world.explored[x, y]:
                    resources = world.resources[(x, y)]
                    if resources['food'] > 0:
                        f_text = map_font.render('F', True, (255, 0, 0))
                        screen.blit(f_text, (y * CELL_SIZE + 4, x * CELL_SIZE + 4))
                    if resources['wood'] > 0:
                        w_text = map_font.render('W', True, (0, 128, 0))
                        screen.blit(w_text, (y * CELL_SIZE + CELL_SIZE - 36, x * CELL_SIZE + 4))
                    if resources['stone'] > 0:
                        s_text = map_font.render('S', True, (64, 64, 64))
                        screen.blit(s_text, (y * CELL_SIZE + 4, x * CELL_SIZE + CELL_SIZE - 36))
            # Draw agents
            if (x, y) == tribe.location:
                # Draw tribe sprite
                asset_manager.draw_tribe(screen, y * CELL_SIZE + 12, x * CELL_SIZE + 12)
            for agent in tribe.agents:
                if isinstance(agent, Gatherer):
                    pos = getattr(agent, 'working_location', None) or getattr(agent, 'current_pos', None)
                    if pos == (x, y):
                        # Draw gatherer sprite (on top of tribe if on tribe tile)
                        asset_manager.draw_gatherer(screen, y * CELL_SIZE + 20, x * CELL_SIZE + 20)
            if any(isinstance(agent, Scout) and getattr(agent, 'current_pos', None) == (x, y) for agent in tribe.agents):
                # Draw scout sprite (on top of everything)
                asset_manager.draw_scout(screen, y * CELL_SIZE + 16, x * CELL_SIZE + 16)