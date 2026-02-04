import os
import pygame

class MenuButton:
    def __init__(self, text, x, y, width, height, font, assets_path=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.screenshot = None
        self.color = (100, 100, 100)  # Default Gray
        screenshot_name = self.text.lower().replace(" ", "_") + "_screenshot.png"
        if assets_path:
            screenshot_path = os.path.join(assets_path, "screenshots", screenshot_name)
            if os.path.exists(screenshot_path):
                self.screenshot = pygame.image.load(screenshot_path).convert()
                self.screenshot = pygame.transform.scale(self.screenshot, (width, height))
            else:
                self.screenshot = None
        else:
            print(f"No assets path provided for {self.text}, skipping screenshot load.") 


        

    def draw(self, screen, is_selected):
        # Draw the button rectangle
        if is_selected:
            scaled_copy = self.rect.inflate(10, 10)
            pygame.draw.rect(screen, (18, 171, 219), scaled_copy)
            pygame.draw.rect(screen, (200, 200, 200), self.rect)
            if self.screenshot:
                screen.blit(self.screenshot, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
            if self.screenshot:
                screen.blit(self.screenshot, self.rect)
            temp_surface = pygame.Surface((self.rect.width, self.rect.height))
            temp_surface.set_alpha(150)
            temp_surface.fill((0, 0, 0))
            screen.blit(temp_surface, self.rect.topleft)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Border
        
        # Render the text
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center + pygame.Vector2(0, self.rect.height // 2 + 30))
        screen.blit(text_surf, text_rect)
