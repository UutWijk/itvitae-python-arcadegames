import pygame

class State:
    def __init__(self, screen, multiplayer=False):
        self.screen = screen
        self.next_state = None
        self.multiplayer = multiplayer

        # standard key map for up, down, left, right, a, b
        self.key_map = {
        pygame.K_UP: "up", pygame.K_DOWN: "down",
        pygame.K_LEFT: "left", pygame.K_RIGHT: "right",
        pygame.K_a: "a", pygame.K_b: "b"
        }

        # substitute controls for multiplayer
        # ESDF for player 1 (instead of WASD which would use the A button)
        if self.multiplayer:
            self.key_map = {
        pygame.K_e: "up", pygame.K_d: "down",
        pygame.K_s: "left", pygame.K_f: "right",
        pygame.K_a: "a", pygame.K_b: "b",
        pygame.K_UP: "up2", pygame.K_DOWN: "down2",
        pygame.K_LEFT: "left2", pygame.K_RIGHT: "right2"
        }
            
        # use these dictionaries for key input detection in your game
        # pressed = True while holding key
        # just_pressed = True only for one frame (useful for one shot triggers)
        self.pressed = {key: False for key in self.key_map.values()}
        self.just_pressed = {key: False for key in self.key_map.values()}

    # handles key inputs for self.pressed and self.just_pressed
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_map:
                val = self.key_map[event.key]
                self.pressed[val] = True
                self.just_pressed[val] = True
                
        elif event.type == pygame.KEYUP:
            if event.key in self.key_map:
                val = self.key_map[event.key]
                self.pressed[val] = False

    # implement update in your game class for game logic
    # dt = time interval in seconds (0.01667 on 60FPS)
    def update(self, dt):
        pass

    # implement draw in your game class for visual rendering
    def draw(self):
        pass

    # makes sure just_pressed only triggers once
    def reset_just_pressed(self):
        for key in self.just_pressed:
            self.just_pressed[key] = False