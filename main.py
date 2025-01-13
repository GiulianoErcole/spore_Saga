# main.py
import pygame
import sys
import os

# Initialize Pygame and its font system
pygame.init()
pygame.font.init()

# Initialize sound mixer
pygame.mixer.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spore Saga")

# Create and fill the background with a gradient
background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
for y in range(SCREEN_HEIGHT):
    color_value = int(255 * (1 - y / SCREEN_HEIGHT))
    pygame.draw.line(background, (0, color_value // 2, color_value), 
                    (0, y), (SCREEN_WIDTH, y))

# Load assets
def load_image(name):
    try:
        path = os.path.join('assets', 'images', name)
        return pygame.image.load(path).convert_alpha()
    except:
        return create_default_sprite(name)

def load_sound(name):
    try:
        path = os.path.join('assets', 'sounds', name)
        return pygame.mixer.Sound(path)
    except:
        return None

def create_default_sprite(name):
    if name == 'spore.png':
        surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(surface, (0, 255, 0), (20, 20), 20)
        return surface
    elif name == 'platform.png':
        surface = pygame.Surface((100, 20), pygame.SRCALPHA)
        pygame.draw.rect(surface, (139, 69, 19), (0, 0, 100, 20))
        return surface

# Load assets
player_image = load_image('spore.png')
platform_image = load_image('platform.png')
jump_sound = load_sound('jump.wav')
collect_sound = load_sound('collect.wav')
powerup_sound = load_sound('powerup.wav')

# Import game classes
from game.world import WorldEnhanced

# Set up the world
world = WorldEnhanced(screen, SCREEN_WIDTH, SCREEN_HEIGHT, 
                     [player_image, platform_image],
                     [jump_sound, collect_sound, powerup_sound])

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Update game state
    world.update()

    # Draw everything
    screen.blit(background, (0, 0))
    world.draw(screen)
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
