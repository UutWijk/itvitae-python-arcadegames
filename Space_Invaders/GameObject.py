import pygame
from abc import ABC, abstractmethod

class GameObject(ABC):
    @abstractmethod
    def update(self, delta: float):
        pass

    @abstractmethod
    def draw(self, surface: pygame.surface):
        pass
