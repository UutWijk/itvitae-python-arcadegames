import pygame
from .constants import Constants

# Class definition of Paddle class; inherits from pygame.Rect
class Paddle(pygame.Rect):
    def __init__(self, x, y, width, height, speed, color, up_key, down_key):
        # initialize the parent class 
        super().__init__(x, y, width, height)
        # Attributes of Paddle objects
        self.speed = speed
        self.color = color 
        self.up_key = up_key
        self.down_key = down_key

        # Created again for usage in this class without importing Pong class
        self.screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()

    # Draw method for Paddle Objects
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)

    # Movement method for Paddle Objects 
    def move(self, screen_height):
        # Get all keys currently being held down
        keys = pygame.key.get_pressed()

        # Object movement using up and down arrows (joystick in Arcade Closet)
        if keys[self.up_key]:
            self.y -= self.speed
        if keys[self.down_key]:
            self.y += self.speed
        
        # Make paddles clamp in place
        self.clamp_ip(self.screen_rect)

        # OPTIONAL ---------------------------
        # Make paddles wrap around the screen
        # if self.bottom < 0:
        #     self.top = screen_height
        # elif self.top > screen_height:
        #     self.bottom = 0
