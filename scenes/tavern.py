import pygame

class TavernScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        #cargar la imagen de fondo de la taberna
        self.background = pygame.image.load("assets/backgrounds/tavern.png").convert()

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))
  
