import pygame
from mecanicas.Player import Player
from mecanicas.npc import NPC   
from mecanicas.inventario import Inventario
from mecanicas.status import Status
from mecanicas.wallet import Wallet

class YardScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.player = Player(100, 100)
        self.wallet = Wallet(creditos_iniciales=1000)
        self.inventario = Inventario(self.wallet)
        self.status = Status(max_health=100)

        #carga del fondo 

        self.background = pygame.image.load("assets/backgrounds/yard1.png").convert() 
        #posicion incial del jugador en el patio de la taberna
        self.player.x = 200
        self.player.y = 250

        #colisiones del entorno
        self.obstaculos = [
           pygame.Rect(93, 480, 260, 42),  # zona 1
            pygame.Rect(20, 2, 216, 100),  # zona 2
            pygame.Rect(811, 11, 156, 195),  # zona 3
            pygame.Rect(802, 589, 175, 115),  # zona 4
            pygame.Rect(82, 442, 164, 53),  # zona 5
            pygame.Rect(167, 518, 164, 33),  # zona 6

        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Abrir/cerrar inventario
            if event.key == pygame.K_i:
                self.inventario.toggle()
                return

            if self.inventario.visible:
                return
        if event.type == pygame.KEYDOWN:
            #status con shift
            if event.key == pygame.K_LSHIFT:
                self.status.toggle()
                return

    def update(self, dt):
        if self.inventario.visible:
            return
        old_x = self.player.x
        old_y = self.player.y

        self.player.update(dt)
        self.status.update(dt)

        for obstacul in self.obstaculos:
            if self.player.rect.colliderect(obstacul):
                self.player.x = old_x
                self.player.y = old_y
                self.player.rect.topleft = (self.player.x, self.player.y)

        #regresar a la escena anterior
        if self.player.y < -50:
            from scenes.tavernYard import TavernYardScene
            self.game.change_scene(TavernYardScene(self.game))


    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        self.inventario.draw(self.screen)
        self.status.draw(self.screen)
    
        for obstaculo in self.obstaculos:
            pygame.draw.rect(self.screen, (255, 0, 0), obstaculo, 2)
            pygame.draw.rect(self.screen, (0, 255, 0), self.player.rect, 2)
            #for npc in self.npcs:
             #       pygame.draw.rect(self.screen, (0, 0, 255), npc.rect, 2)
