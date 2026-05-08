import pygame
from mecanicas.Player import Player
from mecanicas.npc import NPC   
from mecanicas.inventario import Inventario
from mecanicas.status import Status
from mecanicas.wallet import Wallet
from mecanicas.women import WomanNPC

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
           pygame.Rect(138, 440, 108, 90),  # zona 1
            pygame.Rect(248, 438, 20, 102),  # zona 2
            pygame.Rect(273, 477, 43, 92),  # zona 3
            pygame.Rect(83, 443, 73, 78),  # zona 4
            pygame.Rect(35, 17, 185, 40),  # zona 5
            pygame.Rect(822, 5, 162, 205),  # zona 6
        ]
        #coliciones de la mujer
        self.women_obstaculos = [
            pygame.Rect(450, 300, 128, 128),  # zona de la mujer
        ]



        #cargando npcs con wallet conectado
        self.npcs = [
            NPC(590, 340, "bardo", wallet=self.wallet),
        ]
        #cargando npcs de mujer
        self.women_npcs = [
            WomanNPC(450, 300, "plebe", wallet=self.wallet),
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

        for women_obstacul in self.women_obstaculos:
            if self.player.rect.colliderect(women_obstacul):
                self.player.x = old_x
                self.player.y = old_y
                self.player.rect.topleft = (int(old_x), int(old_y))

        #regresar a la escena anterior
        if self.player.y < -50:
            from scenes.tavernYard import TavernYardScene
            self.game.change_scene(TavernYardScene(self.game))


    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        self.inventario.draw(self.screen)
        self.status.draw(self.screen)

        #añadiremos el sprite de mujer 
        self.women_npcs[0].draw(self.screen)       

        for woman_npc in self.women_npcs:
            woman_npc.draw(self.screen)

        for obstaculo in self.obstaculos:
            pygame.draw.rect(self.screen, (255, 0, 0), obstaculo, 2)
            pygame.draw.rect(self.screen, (0, 255, 0), self.player.rect, 2)
            #for npc in self.npcs:
             #       pygame.draw.rect(self.screen, (0, 0, 255), npc.rect, 2)
            for woman_npc in self.women_npcs:
                    pygame.draw.rect(self.screen, (255, 0, 255), woman_npc.rect, 2)
