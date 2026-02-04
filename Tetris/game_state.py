import pygame

MOVE_PIECE_EVENT = pygame.USEREVENT + 1

class game_continues:
    def __init__(self) -> None:
        self.game_continues = True        

class left_timer:
    def __init__(self) -> None:
        self.left_timer = 5

class right_timer:
    def __init__(self) -> None:
        self.right_timer = 5        

class Timer:
    def __init__(self) -> None:
        self.speed = 1000

    def start(self) -> None:
        pygame.time.set_timer(MOVE_PIECE_EVENT, self.speed)

    def set_speed(self, speed) -> None:
        self.speed = speed
        self.start()
    
    def set_start_speed(self) -> None:
        self.speed = 1000
        self.start()

timer = Timer()
"""global timer for the game speed"""
def make_timer() -> None:
    global timer
    timer.start()
