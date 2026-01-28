import pygame


MOVE_PIECE_EVENT = pygame.USEREVENT + 1

class Score:
    def __init(self):
        self.score = 0

score = Score()

class Timer:
    def __init__(self):
        self.speed = 1000

    def start(self):
        pygame.time.set_timer(MOVE_PIECE_EVENT, self.speed)

    def set_speed(self, speed):
        self.speed = speed

        self.start()

    def speed(self):
        return self.speed
    
    def set_start_speed(self):
        self.speed = 1000
        self.start()

    def update_speed(self): 
        current_score = score
        # print(current_score)

timer = Timer()
def make_timer():
    global timer
    timer.start()
