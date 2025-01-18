import pygame
from random import randint
from .player import Player
from .platform import Platform
from .collectible import Collectible

class WorldEnhanced:
    def __init__(self, screen, width, height, images, sounds=None):
        self.screen = screen
        self.width = width
        self.height = height
        self.player_image, self.platform_image = images
        self.sounds = sounds
        
        # Create player
        self.player = Player(self.player_image, 100, 300, sounds)
        
        # Create level elements
        self.platforms = self.create_level()
        self.collectibles = []
        self.spawn_collectibles()
        
        # Score system
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        
        # Background layers for parallax
        self.bg_layers = [
            pygame.Surface((width, height), pygame.SRCALPHA) for _ in range(3)
        ]
        self.setup_background_layers()

    def create_level(self):
        platforms = [
            Platform(self.platform_image, 0, 550, 200, 20),
            Platform(self.platform_image, 250, 450, 200, 20),
            Platform(self.platform_image, 500, 350, 200, 20),
            Platform(self.platform_image, 200, 250, 200, 20),
            Platform(self.platform_image, 600, 200, 100, 20),
            Platform(self.platform_image, 400, 150, 100, 20),
            Platform(self.platform_image, -50, self.height - 20, 900, 20)
        ]
        
        # Make some platforms moving
        platforms[2].moving = True
        platforms[4].moving = True
        
        return platforms
        
    def setup_background_layers(self):
        for layer in self.bg_layers:
            for i in range(0, self.width, 100):
                height = randint(50, 150)
                points = [(i, self.height), (i + 50, self.height - height), 
                         (i + 100, self.height)]
                if layer == self.bg_layers[0]:
                    color = (30, 30, 50, 100)
                elif layer == self.bg_layers[1]:
                    color = (40, 40, 60, 100)
                else:
                    color = (50, 50, 70, 100)
                pygame.draw.polygon(layer, color, points)
    
    def spawn_collectibles(self):
        for platform in self.platforms:
            if randint(0, 1):
                x = platform.rect.centerx
                y = platform.rect.top - 30
                self.collectibles.append(Collectible(x, y))
                
        for _ in range(3):
            x = randint(0, self.width)
            y = randint(100, self.height - 100)
            self.collectibles.append(Collectible(x, y, "power"))
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move(-1)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move(1)
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.jump()
        if keys[pygame.K_LSHIFT]:
            self.player.dash(pygame.time.get_ticks())
    
    def update(self):
        self.handle_input()
        
        # Update platforms
        for platform in self.platforms:
            platform.update()
        
        # Update player
        self.player.update(self.platforms)
        
        # Update collectibles
        for collectible in self.collectibles[:]:
            if not collectible.collected:
                collectible.update()
                if self.player.rect.colliderect(collectible.rect):
                    collectible.collected = True
                    if collectible.type == "spore":
                        self.score += 100
                        if self.sounds and self.sounds[1]:  # collect sound
                            self.sounds[1].play()
                    elif collectible.type == "power":
                        self.player.is_powered_up = True
                        self.player.power_up_time = pygame.time.get_ticks()
                        self.player.JUMP_SPEED *= 1.5
                        if self.sounds and self.sounds[2]:  # powerup sound
                            self.sounds[2].play()
        
        # Update power-up status
        if self.player.is_powered_up and pygame.time.get_ticks() - self.player.power_up_time > 5000:
            self.player.is_powered_up = False
            self.player.JUMP_SPEED = -15  # Reset to normal
        
        # Screen boundaries
        if self.player.rect.left < 0:
            self.player.rect.left = 0
        if self.player.rect.right > self.width:
            self.player.rect.right = self.width
        if self.player.rect.top < 0:
            self.player.rect.top = 0
            
        # Reset player if they fall off
        if self.player.rect.top > self.height:
            self.player.rect.x = 100
            self.player.rect.y = 300
            self.score = max(0, self.score - 50)  # Penalty for falling
    
    def draw(self, screen):
        # Draw parallax background
        screen_scroll = -self.player.velocity_x * 0.1
        for i, layer in enumerate(self.bg_layers):
            scroll_amount = screen_scroll * (i + 1) * 0.5
            screen.blit(layer, (scroll_amount, 0))
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(screen)
        
        # Draw collectibles
        for collectible in self.collectibles:
            if not collectible.collected:
                collectible.draw(screen)
        
        # Draw player
        self.player.draw(screen)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Draw power-up timer if active
        if self.player.is_powered_up:
            time_left = 5 - (pygame.time.get_ticks() - self.player.power_up_time) / 1000
            if time_left > 0:
                timer_text = self.font.render(f'Power-up: {time_left:.1f}s', True, (255, 215, 0))
                screen.blit(timer_text, (10, 50))
