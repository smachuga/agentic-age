# Chat Window for Stone Age Agents
import pygame
from map import WINDOW_WIDTH, WINDOW_HEIGHT

class ChatWindow:
    def __init__(self, font, max_messages=50, visible_messages=10):
        self.font = font
        self.messages = []
        self.max_messages = max_messages
        self.visible_messages = visible_messages
        self.window_height = 200
        self.window_y = WINDOW_HEIGHT - self.window_height
    
    def add_message(self, message, sender="Chief"):
        """Add a message to the chat window"""
        formatted_message = f"{sender} says {message}"
        self.messages.append(formatted_message)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)  # Remove oldest message
    
    def draw(self, screen):
        """Draw the chat window on the screen"""
        # Semi-transparent background
        chat_surface = pygame.Surface((WINDOW_WIDTH, self.window_height))
        chat_surface.set_alpha(200)
        chat_surface.fill((15, 15, 25))  # Dark blue-ish background
        screen.blit(chat_surface, (0, self.window_y))
        
        # Border
        pygame.draw.rect(screen, (100, 100, 150), (0, self.window_y, WINDOW_WIDTH, self.window_height), 2)
        
        # Title bar
        title_surface = pygame.Surface((WINDOW_WIDTH, 25))
        title_surface.set_alpha(220)
        title_surface.fill((50, 50, 80))
        screen.blit(title_surface, (0, self.window_y))
        pygame.draw.line(screen, (100, 100, 150), (0, self.window_y + 25), (WINDOW_WIDTH, self.window_y + 25), 1)
        
        title_text = self.font.render("Game Chat", True, (255, 255, 255))
        screen.blit(title_text, (10, self.window_y + 3))
        
        # Draw chat messages (most recent at bottom)
        y_pos = self.window_y + 35  # Start below title bar
        messages_to_show = min(len(self.messages), self.visible_messages)
        
        for i in range(len(self.messages) - messages_to_show, len(self.messages)):
            if y_pos > self.window_y + self.window_height - 10:  # Leave room at bottom
                break
            message = self.messages[i]
            text = self.font.render(message, True, (220, 220, 220))
            screen.blit(text, (10, y_pos))
            y_pos += 20