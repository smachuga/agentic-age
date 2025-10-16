# Game module for Stone Age Agents
import pygame
import sys
from world import World
from tribe import Tribe
from scout import Scout
from gatherer import Gatherer
from map import *

def draw_status(screen, tribe, font, asset_manager, show_tribe_info):
    # Tribe info bar at top left with small icons
    x_offset = 10
    y_offset = 10
    
    # Tribe name
    tribe_text = font.render(f"Tribe {tribe.name}", True, (255, 255, 255))
    screen.blit(tribe_text, (x_offset, y_offset))
    x_offset += tribe_text.get_width() + 15
    
    # Food
    asset_manager.draw_food_small(screen, x_offset, y_offset)
    food_text = font.render(str(tribe.food), True, (255, 255, 255))
    screen.blit(food_text, (x_offset + 50, y_offset))
    x_offset += 90
    
    # Wood
    asset_manager.draw_wood_small(screen, x_offset, y_offset)
    wood_text = font.render(str(tribe.wood), True, (255, 255, 255))
    screen.blit(wood_text, (x_offset + 40, y_offset))
    x_offset += 80
    
    # Stone
    asset_manager.draw_stone_small(screen, x_offset, y_offset)
    stone_text = font.render(str(tribe.stone), True, (255, 255, 255))
    screen.blit(stone_text, (x_offset + 30, y_offset))
    x_offset += 60
    
    # Morale (using happy icon)
    asset_manager.draw_happy_small(screen, x_offset, y_offset)
    morale_text = font.render(str(tribe.morale), True, (255, 255, 255))
    screen.blit(morale_text, (x_offset + 25, y_offset))
    x_offset += 80
    
    # Population (using population icon)
    asset_manager.draw_population_small(screen, x_offset, y_offset)
    pop_text = font.render(str(tribe.population), True, (255, 255, 255))
    screen.blit(pop_text, (x_offset + 35, y_offset))
    x_offset += 80
    
    # Health (using icon)
    asset_manager.draw_health_small(screen, x_offset, y_offset)
    health_text = font.render(str(tribe.health), True, (255, 255, 255))
    screen.blit(health_text, (x_offset + 30, y_offset))
    
    # Tribe info dropdown
    if show_tribe_info:
        dropdown_y = 45  # Below the main status bar
        
        # Semi-transparent background for dropdown
        dropdown_height = 150
        dropdown_surface = pygame.Surface((WINDOW_WIDTH - 20, dropdown_height))
        dropdown_surface.set_alpha(220)
        dropdown_surface.fill((20, 20, 20))
        screen.blit(dropdown_surface, (10, dropdown_y))
        
        # Border
        pygame.draw.rect(screen, (100, 100, 100), (10, dropdown_y, WINDOW_WIDTH - 20, dropdown_height), 2)
        
        # Detailed tribe information
        detail_lines = [
            f"Detailed Tribe Information - {tribe.name}",
            "",
            f"Resources: Food {tribe.food} | Wood {tribe.wood} | Stone {tribe.stone}",
            f"Status: Population {tribe.population} | Morale {tribe.morale} | Health {tribe.health}",
            "",
            "Agents:"
        ]
        
        # Add agent details
        for agent in tribe.agents:
            status_lines = agent.status().split('\n')
            detail_lines.append(f"  {status_lines[0]}")
            for line in status_lines[1:]:
                detail_lines.append(f"    {line}")
        
        # Render dropdown content
        y_pos = dropdown_y + 10
        for line in detail_lines:
            if line.startswith("Detailed Tribe Information"):
                text = font.render(line, True, (255, 255, 0))  # Yellow for title
            else:
                text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (20, y_pos))
            y_pos += 20
    
    # Agent status at bottom (status window) - only show when dropdown is closed
    if not show_tribe_info:
        y = WINDOW_HEIGHT - 200
        
        # Find the scout
        scout = None
        for agent in tribe.agents:
            if isinstance(agent, Scout):
                scout = agent
                break
        if scout:
            scout_text = font.render(f"Scout: at {scout.current_pos}", True, (255, 255, 255))
            screen.blit(scout_text, (10, y))
            y += 25
        
        # Find the gatherer
        gatherer = None
        for agent in tribe.agents:
            if isinstance(agent, Gatherer):
                gatherer = agent
                break
        if gatherer:
            status = f"Gatherer: "
            if gatherer.returning:
                status += f"returning from {gatherer.working_location} with {sum(gatherer.carrying.values())} resources"
            elif gatherer.working_location:
                status += f"gathering at {gatherer.working_location}, progress {gatherer.gathering_progress}/{gatherer.gathering_target}, carrying {sum(gatherer.carrying.values())}"
            else:
                status += "idle at tribe"
            gatherer_text = font.render(status, True, (255, 255, 255))
            screen.blit(gatherer_text, (10, y))

def draw_overlay(screen, tribe, overlay_font, asset_manager):
    overlay_x = 50
    overlay_y = 50
    overlay_width = 500
    overlay_height = 300
    
    # Semi-transparent background
    overlay_surface = pygame.Surface((overlay_width, overlay_height))
    overlay_surface.set_alpha(200)
    overlay_surface.fill((0, 0, 0))
    screen.blit(overlay_surface, (overlay_x, overlay_y))
    
    pygame.draw.rect(screen, (0, 0, 0), (overlay_x, overlay_y, overlay_width, overlay_height), 2)  # Border
    
    # Title bar
    pygame.draw.rect(screen, (100, 149, 237), (overlay_x, overlay_y, overlay_width, 40))
    pygame.draw.line(screen, (70, 130, 180), (overlay_x, overlay_y + 40), (overlay_x + overlay_width, overlay_y + 40), 2)
    
    lines = []
    lines.append("TRIBE INFORMATION")
    lines.append("")
    lines.append(f"Tribe: {tribe.name}")
    lines.append(f"Population: {tribe.population} | Morale: {tribe.morale} | Health: {tribe.health}")
    lines.append("")
    lines.append("AGENTS:")
    
    for agent in tribe.agents:
        status_lines = agent.status().split('\n')
        lines.append(status_lines[0])
        for line in status_lines[1:]:
            lines.append(f"  {line}")
    
    # Render
    y_offset = 70  # Start after title bar and icons
    for line in lines:
        if line == "TRIBE INFORMATION":
            text = overlay_font.render(line, True, (255, 255, 255))  # White on blue
            screen.blit(text, (overlay_x + 20, overlay_y + 10))
            
            # Draw resource icons
            # Food: sprite
            asset_manager.draw_food(screen, overlay_x + 15, overlay_y + 35)
            food_text = overlay_font.render(str(tribe.food), True, (255, 255, 255))
            screen.blit(food_text, (overlay_x + 55, overlay_y + 45))
            
            # Wood: sprite
            asset_manager.draw_wood(screen, overlay_x + 100, overlay_y + 40)
            wood_text = overlay_font.render(str(tribe.wood), True, (255, 255, 255))
            screen.blit(wood_text, (overlay_x + 140, overlay_y + 45))
            
            # Stone: sprite
            asset_manager.draw_stone(screen, overlay_x + 180, overlay_y + 40)
            stone_text = overlay_font.render(str(tribe.stone), True, (255, 255, 255))
            screen.blit(stone_text, (overlay_x + 220, overlay_y + 45))
        else:
            text = overlay_font.render(line, True, (255, 255, 255))
            screen.blit(text, (overlay_x + 20, overlay_y + y_offset))
            y_offset += 20