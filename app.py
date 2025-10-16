# --- Pygame Integration ---
import pygame
import sys
from world import World
from tribe import Tribe
from scout import Scout
from gatherer import Gatherer
from game import *
from assets import AssetManager
from map import CELL_SIZE, MAP_WIDTH, MAP_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT
from chat_window import ChatWindow

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Stone Age Agents Prototype")
    font = pygame.font.SysFont(None, 28)
    map_font = pygame.font.SysFont(None, 36)
    show_tribe_info = False
    
    asset_manager = AssetManager()
    asset_manager.load_assets()
    
    world = World(width=MAP_WIDTH, height=MAP_HEIGHT)
    tribe = Tribe("Human Tribe", starting_location=(MAP_HEIGHT // 2, MAP_WIDTH // 2))
    # Set tribe tile to special terrain
    world.map[tribe.location[0], tribe.location[1]] = 'tribe'
    # Remove resources from tribe tile
    world.resources[tribe.location] = {'food': 0, 'wood': 0, 'stone': 0}
    tribe.add_agent(Scout(world))
    tribe.add_agent(Gatherer(world))
    # Mark tribe location as explored
    world.explored[tribe.location[0], tribe.location[1]] = True

    # Create chat window
    chat_window = ChatWindow(font)
    
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                direction = None
                if event.key == pygame.K_UP:
                    direction = "north"
                elif event.key == pygame.K_DOWN:
                    direction = "south"
                elif event.key == pygame.K_LEFT:
                    direction = "west"
                elif event.key == pygame.K_RIGHT:
                    direction = "east"
                if direction:
                    result = tribe.issue_directive(Scout, "scout", direction)
                    if result:
                        chat_window.add_message(result, "Scout")
                elif event.key == pygame.K_g:
                    # Send gatherer to scout's current location to gather food
                    scout_pos = None
                    for agent in tribe.agents:
                        if isinstance(agent, Scout):
                            scout_pos = agent.current_pos
                            break
                    if scout_pos:
                        result = tribe.issue_directive(Gatherer, "gather", scout_pos)
                        if result:
                            chat_window.add_message(result, "Gatherer")
                    else:
                        chat_window.add_message("No scout found to follow.")
                elif event.key == pygame.K_r:
                    # Send gatherer back to tribe
                    result = tribe.issue_directive(Gatherer, "return")
                    if result:
                        chat_window.add_message(result, "Gatherer")
                elif event.key == pygame.K_t:
                    # Toggle tribe info dropdown
                    show_tribe_info = not show_tribe_info
                elif event.key == pygame.K_q:
                    running = False

        # Process scout exploration timer
        for agent in tribe.agents:
            if isinstance(agent, Scout) and agent.exploration_timer > 0:
                agent.exploration_timer -= 1
                if agent.exploration_timer == 0:
                    x, y = agent.current_pos
                    world.explored[x, y] = True
                    # Update memory with resources
                    live_resources = world.resources.get(agent.current_pos, {'food': 0, 'wood': 0, 'stone': 0})
                    tribe.update_memory("scout_report", {agent.current_pos: live_resources})
                    chat_window.add_message(f"I discovered {live_resources['food']} food, {live_resources['wood']} wood, {live_resources['stone']} stone at {agent.current_pos}", "Scout")

        # Process gatherer ticks
        for agent in tribe.agents:
            if hasattr(agent, 'gather_tick'):
                result = agent.gather_tick()
                if result:
                    chat_window.add_message(result, "Gatherer")

        screen.fill((0, 0, 0))
        draw_map(screen, world, tribe, map_font, asset_manager)
        draw_status(screen, tribe, font, asset_manager, show_tribe_info)
        
        # Draw chat window
        chat_window.draw(screen)
        chat_window.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()