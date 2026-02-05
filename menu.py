import pygame
from game import Game
from state import State
from menubutton import MenuButton
from menupage import Page

import os

class MainMenu(State):
    def __init__(self, screen, games):
        super().__init__(screen)
        self.games = games

        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(current_dir, "menu_assets")
        background_image_path = os.path.join(assets_path, "background", "capgemini_wirl.png")
        self.background_image = pygame.image.load(background_image_path).convert()
        self.capgemini_logo = pygame.image.load(os.path.join(assets_path, "capgemini_logos", "capgemini_logo_blauw_op_wit_rechthoek.png")).convert_alpha()
        self.capgemini_white = pygame.image.load(os.path.join(assets_path, "capgemini_logos", "capgemini_logo_wit.png")).convert_alpha()
        self.academy_white = pygame.image.load(os.path.join(assets_path, "capgemini_logos", "academyfooterlogo.png"))
        self.capgemini_logo = pygame.transform.smoothscale(self.capgemini_logo, (0.5 * self.capgemini_logo.get_width(), 0.5 * self.capgemini_logo.get_height()))
        self.capgemini_white = pygame.transform.smoothscale(self.capgemini_white, (0.5 * self.capgemini_white.get_width(), 0.5 * self.capgemini_white.get_height()))
        self.academy_white = pygame.transform.smoothscale(self.academy_white, (0.2 * self.academy_white.get_width(), 0.2 * self.academy_white.get_height()))
        self.font = pygame.font.Font(os.path.join(assets_path, "fontPixel.ttf"), 35)
        self.pagemarkers_font = pygame.font.Font(os.path.join(assets_path, "fontPixel.ttf"), 70)

        self.page_rows = 2
        self.page_cols = 3
        self.pages = self.create_pages(assets_path)
        self.current_page_index = 0
        self.current_row_index = 0
        self.current_col_index = 0
        self.current_game = self.games[0]
        self.current_index = 0

    def update(self, dt):
        self.switch_button()
        self.current_game = self.pages[self.current_page_index].buttons[self.current_row_index][self.current_col_index].text
        if self.just_pressed["a"]:
            self.next_state = self.current_game




    def switch_button(self):
        def switch_page(direction):
            if direction == "next":
                if self.current_page_index == len(self.pages) - 1:
                    self.current_page_index = 0
                else:
                    self.current_page_index += 1
            elif direction == "prev":
                if self.current_page_index == 0:
                    self.current_page_index = len(self.pages) - 1
                else:
                    self.current_page_index -= 1

        if self.just_pressed["up"]:
            if self.current_row_index == 0:
                self.current_row_index = self.page_rows - 1
            else:
                self.current_row_index -= 1
        if self.just_pressed["down"]:
            if self.current_row_index == self.page_rows - 1:
                self.current_row_index = 0
            else:
                self.current_row_index += 1
        if self.just_pressed["left"]:
            if self.current_col_index == 0:
                self.current_col_index = self.page_cols - 1
                switch_page("prev")
            else:
                self.current_col_index -= 1
        if self.just_pressed["right"]:
            if self.current_col_index == self.page_cols - 1:
                self.current_col_index = 0
                switch_page("next")
            else:
                self.current_col_index += 1
        


    def create_pages(self, assets_path=None):
        pages = []
        games_copy = self.games.copy()
        games_per_page = self.page_rows * self.page_cols
        
        while games_copy:
            chunk = [games_copy.pop(0) for _ in range(min(len(games_copy), games_per_page))]
            new_page = Page(chunk, self.page_rows, self.page_cols, self.screen.get_size(), self.font, assets_path)
            pages.append(new_page)
        return pages

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background_image, (0, 0))
        temp_surface = pygame.Surface((self.screen.width, self.screen.height))
        temp_surface.set_alpha(225)
        temp_surface.fill((0, 112,173))
        self.screen.blit(temp_surface, (0,0))
        self.screen.blit(self.capgemini_white, (50, 50))
        self.screen.blit(self.academy_white, (self.screen.width - 25 - self.academy_white.get_width(), self.screen.height - 25 - self.academy_white.get_height()))        
        current_page = self.pages[self.current_page_index]
        current_page.draw(self.screen, (self.current_row_index, self.current_col_index))


        pagemarkers = [" ", " ", " ", " ", " "] 
        if len(self.pages) > 1:
            if self.current_page_index != 0:
                pagemarkers[0] = "<"
            
            if self.current_page_index != len(self.pages) - 1:
                pagemarkers[4] = ">"

            pagemarkers[2] = str(self.current_page_index + 1)

        pagemarkers = "".join(pagemarkers)
        pagemarkers_surf = self.pagemarkers_font.render(pagemarkers, True, (255, 255, 255))
        pagemarkers_rect = pagemarkers_surf.get_rect()
        self.screen.blit(pagemarkers_surf, ((self.screen.width - pagemarkers_rect.width) // 2, self.screen.height - 150))


        
            
                

