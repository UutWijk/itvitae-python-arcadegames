import os
import pygame

class MenuButton:
    def __init__(self, text, x, y, width, height, font, assets_path=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.screenshot = None
        self.color = (100, 100, 100)  # default gray

        # load screenshot if game has one in the folder
        screenshot_name = self.text.lower().replace(" ", "_") + "_screenshot.png"
        if assets_path:
            screenshot_path = os.path.join(assets_path, "screenshots", screenshot_name)
            if os.path.exists(screenshot_path):
                self.screenshot = pygame.image.load(screenshot_path).convert()
                self.screenshot = pygame.transform.scale(self.screenshot, (width, height))
            else:
                self.screenshot = None



        

    def draw(self, screen, is_selected):
        # light blue outline thats thicker when selected
        scaled_copy = self.rect.inflate(5, 5)
        if is_selected:
            scaled_copy = self.rect.inflate(15, 15)
        pygame.draw.rect(screen, (18, 171, 219), scaled_copy)
        if is_selected:
            scaled_copy = self.rect.inflate(8, 8)
            pygame.draw.rect(screen, (48, 211, 255), scaled_copy)

        # draw screenshot over slightly larger light blue backlayer
        if self.screenshot:
            screen.blit(self.screenshot, self.rect)
            temp_surface = pygame.Surface((self.rect.width, self.rect.height))
            temp_surface.set_alpha(150)
            temp_surface.fill((0, 0, 0))
            screen.blit(temp_surface, self.rect.topleft)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # add thin black border to screenshot
        
        # render the text
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_backlayer_surf = self.font.render(self.text, True, (0, 112, 173))

        # "highlights" text when selected by decreasing opacity of non-selected game names
        if not is_selected:
            text_surf.set_alpha(150)

        
        text_rect = text_surf.get_rect(center=self.rect.center + pygame.Vector2(0, self.rect.height // 2 + 30))
        text_backlayer_rect = text_surf.get_rect(center=self.rect.center + pygame.Vector2(-2, self.rect.height // 2 + 28))

        # adds "shadow" to selected game name
        if is_selected:
            screen.blit(text_backlayer_surf, text_backlayer_rect)
        screen.blit(text_surf, text_rect)
