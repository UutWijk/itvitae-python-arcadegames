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

    def handle_events(self, event):
        for button in self.buttons:
                if button.is_clicked(event):
                    # Trigger the state change using the button's text
                    self.next_state = button.text

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((255, 255, 255))
        for button in self.buttons:
            button.draw(self.screen)

        
