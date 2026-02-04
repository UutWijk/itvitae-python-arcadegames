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

        self.font = pygame.font.SysFont("Arial", 30)

        # UI Layout settings
        start_x = 300
        start_y = 100
        button_h = 50
        spacing = 20  

        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(current_dir, "menu_assets")
        background_image_path = os.path.join(assets_path, "background", "capgemini_wirl.png")
        self.background_image = pygame.image.load(background_image_path).convert()

        self.page_rows = 2
        self.page_cols = 3
        self.pages = self.create_pages(assets_path)
        self.current_page_index = 0
        self.current_row_index = 0
        self.current_col_index = 0
        self.current_game = self.games[0]
        


        self.buttons = []
        for index, name in enumerate(self.games):
            pos_y = start_y + (index * (button_h + spacing))
            new_button = MenuButton(name, start_x, pos_y, 200, button_h, self.font, assets_path)
            self.buttons.append(new_button)
        


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
        current_page = self.pages[self.current_page_index]
        current_page.draw(self.screen, (self.current_row_index, self.current_col_index))

        
            
                

