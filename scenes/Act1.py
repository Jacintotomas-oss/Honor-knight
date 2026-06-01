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
        pygame.Rect(385, 207, 227, 16),  # zona 1
        pygame.Rect(273, 216, 49, 156),  # zona 2
        pygame.Rect(704, 222, 47, 153),  # zona 3
        pygame.Rect(316, 231, 122, 140),  # zona 4
        pygame.Rect(587, 229, 115, 145),  # zona 5
        pygame.Rect(131, 513, 98, 49),  # zona 6
        pygame.Rect(793, 507, 109, 62),  # zona 7
        pygame.Rect(2, 258, 265, 113),  # zona 8
        pygame.Rect(756, 233, 265, 140),  # zona 9
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
            
        
        #cambio de escena
        if self.player.y > 500:
            from scenes.Select import Select_Option
            self.game.change_scene(self.game.get_scene("Select", Select_Option))

        #regresar a la escena anterior
        if self.player.y < 310:
            from scenes.yard import YardScene
            self.game.change_scene(self.game.get_scene("yard",YardScene))
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)


        #for obstaculo in self.obstaculos:
         #   pygame.draw.rect(self.screen, (255, 0, 0), obstaculo, 2)
          #  pygame.draw.rect(self.screen, (0, 255, 0), self.player.rect, 2)
            

        