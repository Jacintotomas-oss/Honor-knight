import pygame
from mecanicas.Player import Player
from mecanicas.npc import NPC



class Cap1:
    def __init__(self,game):
        self.game = game
        self.screen = game.screen
        self.player = Player(100, 100)
        

        self.background = pygame.image.load("assets/backgrounds/cap1.png").convert()

    def handle_event(self,event):
        pass
    def update (self,dt):
        self.player.update(dt)
    def draw (self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)

