import pygame

class State:
    def __init__(self, screen, multiplayer=False):
        self.screen = screen
        self.next_state = None
        self.multiplayer = multiplayer

        # standaard key map voor up, down, left, right, a, b
        self.key_map = {
        pygame.K_UP: "up", pygame.K_DOWN: "down",
        pygame.K_LEFT: "left", pygame.K_RIGHT: "right",
        pygame.K_a: "a", pygame.K_b: "b"
        }

        # substitute controls voor multiplayer (momenteel alleen voor pong en blockade)
        # controls van player 1 zijn ESDF om A en B te behouden, player 2 gebruikt de pijltjes
        # de bindings kunnen eventueel eenvoudig hier aangepast worden
        if self.multiplayer:
            self.key_map = {
        pygame.K_e: "up", pygame.K_d: "down",
        pygame.K_s: "left", pygame.K_f: "right",
        pygame.K_a: "a", pygame.K_b: "b",
        pygame.K_UP: "up2", pygame.K_DOWN: "down2",
        pygame.K_LEFT: "left2", pygame.K_RIGHT: "right2"
        }
            
        # gebruik deze dictionary voor key press detection
        # voorbeeld: 
        # if self.pressed["up"]:
        # just_pressed is voor keys die eenmalig triggeren (zoals schieten waarbij hij maar 1x schiet als je de knop inhoudt)
        self.pressed = {key: False for key in self.key_map.values()}
        self.just_pressed = {key: False for key in self.key_map.values()}

    # het afhandelen van key press events
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

    # update en draw (erf deze methoden voor de game logic)
    def update(self, dt):
        pass
    # gebruik eventueel dt voor tijdsgebonden triggers
    # voorbeeld: 
    # def update(self, dt):
    #   if (condition):
    #       self.timer += dt
    # self.timer telt hier de tijd in seconden
    
    def draw(self):
        pass

    # functionaliteit voor de just_pressed mechanic
    def reset_just_pressed(self):
        for key in self.just_pressed:
            self.just_pressed[key] = False