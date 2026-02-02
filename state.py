import pygame

class State:
    def __init__(self, screen, multiplayer=False):
        self.screen = screen
        self.next_state = None
        self.multiplayer = multiplayer
        self.key_map = {
        pygame.K_UP: "up", pygame.K_DOWN: "down",
        pygame.K_LEFT: "left", pygame.K_RIGHT: "right",
        pygame.K_a: "a", pygame.K_b: "b"
        }

        # substitute controls for multiplayer
        if self.multiplayer:
            self.key_map = {
        pygame.K_e: "up", pygame.K_d: "down",
        pygame.K_s: "left", pygame.K_f: "right",
        pygame.K_a: "a", pygame.K_b: "b",
        pygame.K_UP: "up2", pygame.K_DOWN: "down2",
        pygame.K_LEFT: "left2", pygame.K_RIGHT: "right2"
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