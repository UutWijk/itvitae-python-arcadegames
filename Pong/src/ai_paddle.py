from .paddle import Paddle
from .constants import Constants

# Child class definition of the AI paddle opponent 
class AIPaddle(Paddle):
    def __init__(self, x, y, width, height, color, difficulty="easy"): # initialize default difficulty parameter as "easy"
        # attributes of AI paddle
        self.difficulty = difficulty
        
        if difficulty == "easy":
            speed = Constants.AI_SPEED -3   # Slower
            self.deadzone = 16              # Stops early
            self.reaction_limit = 0.5       # Reacts when ball corsses middle line
   
        else: # when difficulty is "hard"
            speed = Constants.AI_SPEED      # Normal AI speed
            self.deadzone = 8               # Precise
            self.reaction_limit = 0.2       # Reacts almost immidiatly
        # Initialize the parent Paddle class
        super().__init__(x, y, width, height, speed, color, None, None)
        

    def move(self, ball):
        # Before moving, check if ball is moving right and where it is on the playing field
        if ball.speed_x > 0 and ball.centerx > Constants.SCREEN_WIDTH * self.reaction_limit:
            
            # Calculate vertical distance between ball and paddle center
            distance = ball.centery - self.centery
            
            # The deadzone makes sure the paddle doesnt keep alligning to the exact pixels of the ball center. It follows 
            # the movement of the ball
            if abs(distance) > self.deadzone:
                if distance > 0:
                    self.y += self.speed
                else:
                    self.y -= self.speed
        
        else:
            # When the AI has returned the ball or when scored: AI returns to center
            screen_center_y = Constants.SCREEN_HEIGHT // 2
            
            if abs(self.centery - screen_center_y) > self.deadzone:
                if self.centery < screen_center_y:
                    self.y += self.speed / 2  # Drift back at half speed
                else:
                    self.y -= self.speed / 2

        # Ensure the paddle stays within screen boundaries
        self.clamp_ip(self.screen_rect)