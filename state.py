from abc import ABC, abstractmethod

class State(ABC):
    def __init__(self, screen):
        self.screen = screen
        self.next_state = None

    @abstractmethod
    def handle_events(self, event):
        pass
    
    @abstractmethod
    def update(self, dt):
        pass
    
    @abstractmethod
    def draw(self):
        pass