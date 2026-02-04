import pygame 
import random 
import os 
from .constants import Constants

# Class definition of Ball objects; inherits from pygame.Rect
class Ball(pygame.Rect): 
    def __init__(self, x, y, size, speed):
        # Initialize parent Class pygame.Rect
        super().__init__(x, y, size, size)

        # Ball speed attributes
        self.base_speed = speed
        self.speed_y = self.base_speed * random.choice([-1, 1])
        self.speed_x = self.base_speed * random.choice([-1, 1])

        self.acceleration = 1.2 # ball moves faster after every paddle hit
        self.max_speed = 28 # prevents unwinnable speeds

        # For making the ball wait (delay) after scoring
        self.waiting = True
        self.reset_time = 0 
        self.delay_duration = 1750 # Delay in milliseconds

        # Ball color
        self.color = "#FFFDF7"

        # Creating absolute path
        cwd = os.path.dirname(os.path.abspath(__file__))

        # Ball sounds
        self.paddle_sound = pygame.mixer.Sound(os.path.join(cwd, "assets", "sounds", "pong_paddle.mp3"))
        self.paddle_sound.set_volume(0.09)
        self.bounce_sound = pygame.mixer.Sound(os.path.join(cwd, "assets", "sounds", "pong_side.mp3"))
        self.bounce_sound.set_volume(0.08)
    

    # Drawing method for Ball
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)

    # For making the Ball wait after scoring
    def start_timer(self):
        self.waiting = True
        self.reset_time = pygame.time.get_ticks() 
        self.center = ((Constants.SCREEN_WIDTH // 2), (Constants.SCREEN_HEIGHT // 2))

    # Movement method for the Ball
    def move(self, screen_rect):
        # Check if we are currently in a waiting state (after scoring in game loop) 
        if self.waiting:
            # If waiting = True we increase the current waiting time
            current_time = pygame.time.get_ticks()
            if current_time - self.reset_time >= self.delay_duration:
                self.waiting = False # Time is up, start moving!
            else:
                return # Still waiting, skip movement logic
        
        self.x += self.speed_x
        self.y += self.speed_y

        # Make Ball bounce off top and bottom of screen
        if self.top <= screen_rect.top or self.bottom >= screen_rect.bottom:
            self.speed_y *= -1 # This reverses the direction of the ball on the y-axis
            self.bounce_sound.play() # Ball sound when bouncing
        

    def reset(self):
        # Move back to center
        self.center = ((Constants.SCREEN_WIDTH // 2), (Constants.SCREEN_HEIGHT // 2))
        
        # Randomize direction again for the next round
        self.speed_x = self.base_speed * random.choice([-1, 1])
        self.speed_y = random.randint(2, 5) * random.choice([-1, 1])
    
    # collision check method and reactions
    def check_collision(self, paddle_rect):
        if self.colliderect(paddle_rect):
            # When ball collides with padle rect: reverse movement direction and play sound
            self.speed_x *= -1
            self.paddle_sound.play()

            # When below the maximum speed set earlier: increase X and y speeds by acceleration
            if abs(self.speed_x) < self.max_speed:
                self.speed_x *= self.acceleration
                self.speed_y *= self.acceleration

            # Prevents "sticky ball": moves ball to outside of paddle rect when ball is moving
            if self.speed_x > 0:
                self.left = paddle_rect.right
            else: 
                self.right = paddle_rect.left
