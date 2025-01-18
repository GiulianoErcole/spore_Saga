import pygame
import math
from random import randint


class Player:
    def __init__(self, image, x, y, sounds=None):
        # Scale the player image to appropriate size
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Movement properties
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = False
        self.facing_right = True

        # Constants for fine-tuned physics
        self.GRAVITY = 0.7
        self.JUMP_SPEED = -15
        self.MOVE_SPEED = 6
        self.MAX_FALL_SPEED = 15

        # Enhanced abilities
        self.dash_speed = 15
        self.can_dash = True
        self.dash_cooldown = 1000
        self.last_dash_time = 0
        self.power_up_time = 0
        self.is_powered_up = False
        
        # Double jump mechanics
        self.can_double_jump = True

        # Particle system
        self.particles = []

        # Sounds
        self.jump_sound = sounds[0] if sounds else None

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.JUMP_SPEED
            self.on_ground = False
            self.can_double_jump = True
            if self.jump_sound:
                self.jump_sound.play()
        elif self.can_double_jump:
            self.velocity_y = self.JUMP_SPEED
            self.can_double_jump = False
            if self.jump_sound:
                self.jump_sound.play()

    def dash(self, current_time):
        if self.can_dash and current_time - self.last_dash_time > self.dash_cooldown:
            self.velocity_x = self.dash_speed if self.facing_right else -self.dash_speed
            self.can_dash = False
            self.last_dash_time = current_time
            self.add_particles(10)

    def move(self, direction):
        self.velocity_x = direction * self.MOVE_SPEED
        if direction != 0:
            self.facing_right = direction > 0
            if abs(self.velocity_x) > 2:
                self.add_particles(1)

    def add_particles(self, count):
        for _ in range(count):
            particle = {
                'pos': [self.rect.centerx, self.rect.centery],
                'velocity': [randint(-2, 2), randint(-2, 2)],
                'lifetime': 30
            }
            self.particles.append(particle)

    def update_particles(self):
        for particle in self.particles[:]:
            particle['pos'][0] += particle['velocity'][0]
            particle['pos'][1] += particle['velocity'][1]
            particle['lifetime'] -= 1
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)

    def handle_collision(self, platforms):
        self.on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Bottom collision (landing)
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.can_dash = True
                # Top collision
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                # Side collisions
                elif self.velocity_x > 0:
                    self.rect.right = platform.rect.left
                elif self.velocity_x < 0:
                    self.rect.left = platform.rect.right

    def update(self, platforms):
        # Apply gravity
        if not self.on_ground:
            self.velocity_y += self.GRAVITY

        # Limit fall speed
        if self.velocity_y > self.MAX_FALL_SPEED:
            self.velocity_y = self.MAX_FALL_SPEED

        # Update position
        self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x

        # Handle collisions
        self.handle_collision(platforms)

        # Update particles
        self.update_particles()

        # Reset horizontal velocity
        self.velocity_x = 0

    def draw(self, screen):
        # Draw particles
        for particle in self.particles:
            alpha = min(255, particle['lifetime'] * 8)
            particle_color = (0, 255, 0, alpha)
            particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, particle_color, (2, 2), 2)
            screen.blit(particle_surface, particle['pos'])

        # Draw player
        image_to_draw = self.image
        if not self.facing_right:
            image_to_draw = pygame.transform.flip(self.image, True, False)
        screen.blit(image_to_draw, self.rect)
