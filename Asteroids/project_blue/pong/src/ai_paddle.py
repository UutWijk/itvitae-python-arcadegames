from .paddle import Paddle
from .constants import Constants

# Class definition of the AI paddle opponent 
class AIPaddle(Paddle):
    def __init__(self, x, y, width, height, speed, color):
        # Initialize the parent Paddle class
        super().__init__(x, y, width, height, speed, color, None, None)
        
        # Deadzone prevents the paddle from shaking when it's "close enough"
        self.deadzone = 12 # INCREASE to make EASIER

    def move(self, ball):
        """
        AI Logic:
        1. Only tracks the ball if it's moving toward the AI and past the halfway point.
        2. Otherwise, drifts back to the vertical center of the screen.
        """
        
        # Check if ball is moving right (toward AI) and is on the right half of the screen
        if ball.speed_x > 0 and ball.centerx > Constants.SCREEN_WIDTH // 2: # Change to * 0.75 to make easier
            
            # Calculate vertical distance between ball and paddle center
            distance = ball.centery - self.centery
            
            # Only move if the distance is larger than the deadzone
            if abs(distance) > self.deadzone:
                if distance > 0:
                    self.y += self.speed
                else:
                    self.y -= self.speed
        
        else:
            # Idle Logic: If ball is far away or moving away, return to center
            screen_center_y = Constants.SCREEN_HEIGHT // 2
            
            if abs(self.centery - screen_center_y) > self.deadzone:
                if self.centery < screen_center_y:
                    self.y += self.speed / 2  # Drift back at half speed
                else:
                    self.y -= self.speed / 2

        # Ensure the paddle stays within screen boundaries
        self.clamp_ip(self.screen_rect)