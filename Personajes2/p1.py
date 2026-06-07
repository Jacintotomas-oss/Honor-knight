import pygame
from mecanicas.Player import Player

class P1(Player):
    def __init__(self, x, y, speed=200):
        super().__init__(x, y)  # solo x, y como acepta Player
        self.speed = speed

        # Sobreescribir el sprite con el del personaje del prólogo
        idle_raw = pygame.image.load("assets/sprites/p1/p1.png").convert_alpha()
        self.idle_sprite = pygame.transform.scale(idle_raw, (128, 128))
        self.image = self.idle_sprite

        self.rect = pygame.Rect(self.x, self.y, 128, 128)