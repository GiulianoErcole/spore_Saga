import pygame
from random import choice
import math

class Collectible:
    def __init__(self, x, y, type="spore"):
        self.type = type
        self.collected = False
        
        # Create rect for collision
        self.rect = pygame.Rect(x, y, 20, 20)
        
        # Animation variables
        self.float_offset = 0
        self.float_speed = 0.1
        self.original_y = y
        
        # Color based on type
        self.colors = {
            "spore": (0, 255, 0),  # Green for regular spores
            "power": (255, 215, 0)  # Gold for power-ups
        }
    
    def update(self):
        # Floating animation
        self.float_offset = math.sin(pygame.time.get_ticks() * self.float_speed) * 5
        self.rect.y = self.original_y + self.float_offset
    
    def draw(self, screen):
        color = self.colors.get(self.type, (0, 255, 0))
        
        if self.type == "spore":
            # Draw main circle
            pygame.draw.circle(screen, color, self.rect.center, 10)
            # Draw smaller decorative circles
            pygame.draw.circle(screen, (255, 255, 255), 
                             (self.rect.centerx - 3, self.rect.centery - 3), 3)
            pygame.draw.circle(screen, (200, 255, 200), 
                             (self.rect.centerx + 2, self.rect.centery + 2), 2)
        else:  # power-up
            # Draw star shape
            points = []
            for i in range(10):
                angle = math.pi * 2 * i / 10
                radius = 10 if i % 2 == 0 else 5
                x = self.rect.centerx + math.cos(angle) * radius
                y = self.rect.centery + math.sin(angle) * radius
                points.append((x, y))
            pygame.draw.polygon(screen, color, points)
            # Add shimmer effect
            pygame.draw.circle(screen, (255, 255, 255), 
                             (self.rect.centerx - 2, self.rect.centery - 2), 2)
