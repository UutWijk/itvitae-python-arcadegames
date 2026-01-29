import pygame

class State:
    def __init__(self, screen):
        self.screen = screen
        self.next_state = None
        self.key_map = {
        pygame.K_UP: "up", pygame.K_DOWN: "down",
        pygame.K_LEFT: "left", pygame.K_RIGHT: "right",
        pygame.K_a: "a", pygame.K_b: "b"
        }
        self.pressed = {key: False for key in self.key_map.values()}
        self.just_pressed = {key: False for key in self.key_map.values()}

    def handle_events(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key in self.key_map:
                val = self.key_map[event.key]
                self.pressed[val] = True
                self.just_pressed[val] = True # The "Pulse"
                
        elif event.type == pygame.KEYUP:
            if event.key in self.key_map:
                val = self.key_map[event.key]
                self.pressed[val] = False

    
    def update(self, dt):
        pass
    
    def draw(self):
        pass

    def reset_just_pressed(self):
        for key in self.just_pressed:
            self.just_pressed[key] = False