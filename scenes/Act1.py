import pygame
from scenes.menu import MenuScene
from mecanicas.inventario import Inventario
from mecanicas.wallet import Wallet
from mecanicas.Player import Player
from mecanicas.status import Status


class Act1Scene(MenuScene):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.player = Player(100, 100)
        self.wallet = game.wallet
        self.inventario = Inventario(self.wallet)
        self.status = Status(max_health=100)

        #carga del fondo
        self.background = pygame.image.load("assets/backgrounds/sal1.png").convert()
        #posicion del jugador 
        self.player.x = 450
        self.player.y = 350

        #colisicones del entorno
        self.obstaculos = [
            
        pygame.Rect(126, 486, 134, 69),  # zona 1
        pygame.Rect(6, 434, 257, 51),  # zona 2
        pygame.Rect(783, 500, 126, 43),  # zona 3
        pygame.Rect(780, 453, 228, 43),  # zona 4
        pygame.Rect(383, 210, 248, 42),  # zona 5

                                    ]
        

    def handle_event(self, evento):
        pass
    def update(self, dt):
        old_x = self.player.x
        old_y = self.player.y
        self.player.update(dt)
        #coliciones
        for obstaculo in self.obstaculos:
            if self.player.rect.colliderect(obstaculo):
                self.player.x = old_x
                self.player.y = old_y
                self.player.rect.topleft = (self.player.x, self.player.y)
            #regresar a la escena anterior
            pass
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)


        for obstaculo in self.obstaculos:
            pygame.draw.rect(self.screen, (255, 0, 0), obstaculo, 2)
            pygame.draw.rect(self.screen, (0, 255, 0), self.player.rect, 2)
           

        