import pygame
from game import Game
from state import State
from menubutton import MenuButton

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
        
        self.buttons = []
        for index, name in enumerate(self.games):
            pos_y = start_y + (index * (button_h + spacing))
            new_button = MenuButton(name, start_x, pos_y, 200, button_h, self.font)
            self.buttons.append(new_button)
        
        self.current_index = 0

    def update(self, dt):
        self.switch_button()
        if self.just_pressed["a"]:
            self.next_state = self.buttons[self.current_index].text


    def draw(self):
        self.screen.fill((255, 255, 255))
        for index, button in enumerate(self.buttons):
            if index == self.current_index:
                button.color = (200, 200, 200)
            else:
                button.color = (100, 100, 100)
            button.draw(self.screen)

        

    def switch_button(self):
        if self.just_pressed["up"]:
            if self.current_index == 0:
                self.current_index = len(self.buttons) - 1
            else:
                self.current_index -= 1
        if self.just_pressed["down"]:
            if self.current_index == len(self.buttons) - 1:
                self.current_index = 0
            else:
                self.current_index += 1
            
                

