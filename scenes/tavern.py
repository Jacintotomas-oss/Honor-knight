import pygame
from mecanicas.Player import Player

class TavernScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.player = Player(100, 100)

        #cargar la imagen de fondo de la taberna
        self.background = pygame.image.load("assets/backgrounds/tavern.png").convert()

    def handle_event(self, event):
        pass

    def update(self, dt):
        self.player.update(dt)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
  
