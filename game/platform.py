import pygame

class Platform:
    def __init__(self, image, x, y, width=100, height=20):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.platform_type = "normal"
        
        # Movement properties for moving platforms
        self.moving = False
        self.move_speed = 2
        self.move_distance = 100
        self.initial_x = x
        self.initial_y = y
        self.move_direction = 1

    def update(self):
        if self.moving:
            if self.move_direction == 1:
                self.rect.x += self.move_speed
                if self.rect.x > self.initial_x + self.move_distance:
                    self.move_direction = -1
            else:
                self.rect.x -= self.move_speed
                if self.rect.x < self.initial_x:
                    self.move_direction = 1
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
