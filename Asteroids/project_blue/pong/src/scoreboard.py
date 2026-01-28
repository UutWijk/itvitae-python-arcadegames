import pygame
import os # Only needed for commented out Pixel font

# Class definition of Scoreboard objects
class Scoreboard():
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.player_score = 0
        self.opponent_score = 0

        current_dir = os.path.dirname(os.path.abspath(__file__))

        self.font = pygame.font.Font(os.path.join(current_dir, "assets", "fonts", "OCRAEXT.TTF"), 100) 
        self.font_small = pygame.font.Font(os.path.join(current_dir, "assets", "fonts", "OCRAEXT.TTF"), 50) 
    
    # Draw method for the scoreboard
    def draw(self, screen):
        # Turning the score into strings and making a surface with a font
        player_surf = self.font.render(str(self.player_score), True, "#0099ff")
        opp_surf = self.font.render(str(self.opponent_score), True, "#ff6600")

        # Blitting the surfaces (relative to screen width)
        screen.blit(player_surf, (self.screen_width // 4, 30))
        screen.blit(opp_surf, (self.screen_width * 3 // 4, 30))
    
    # Score updating method for the scoreboard
    def update_score(self, is_player): 
        if is_player:
            self.player_score += 1
        else:
            self.opponent_score += 1
