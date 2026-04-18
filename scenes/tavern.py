import pygame
from mecanicas.Player import Player
from mecanicas.npc import NPC
from mecanicas.tavernero import Tavernero
from mecanicas.wallet import wallet
from mecanicas.inventario import Inventario

class TavernScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.player = Player(100, 100)
        self.wallet = wallet(creditos_iniciales=1000)
        self.inventario = Inventario(self.wallet)

        # NPC estático del bardo en la taberna
        self.npcs = [
            NPC(590, 340, "bardo")  # bardo cerca de la barra
        ]
        self.npcs = [
        NPC(590, 340, "bardo"),
        Tavernero()
        ]

        # Cargar la imagen de fondo de la taberna
        self.background = pygame.image.load("assets/backgrounds/tavern.png").convert()

        # Rectángulos de colisión del entorno
        self.obstaculos = [
            pygame.Rect(98, 283, 190, 112),
            pygame.Rect(282, 529, 175, 130),
            pygame.Rect(514, 276, 412, 24),
            pygame.Rect(769, 61, 230, 145),
            pygame.Rect(471, 82, 287, 25),
            pygame.Rect(790, 451, 68, 399),
            pygame.Rect(61, 77, 698, 15),
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            #abrir y cerrar inventario
            if event.key == pygame.K_i:
                self.inventario.toggle()
                return
            if self.inventario.visible:
                return  # Si el inventario está abierto, no procesar otras teclas

            # E — activar diálogo o cerrar respuesta
            if event.key == pygame.K_e:
                for npc in self.npcs:
                    distancia = abs(npc.rect.centerx - self.player.rect.centerx) + \
                                abs(npc.rect.centery - self.player.rect.centery)
                    if distancia < 150:
                        if npc.respuesta_activa:
                            npc.cerrar_respuesta()
                        else:
                            npc.activar()

            # R — cerrar diálogo
            if event.key == pygame.K_r:
                for npc in self.npcs:
                    npc.hablando = False
                    npc.nodo_actual = "inicio"
                    npc.esperando_opcion = False
                    npc.respuesta_activa = None

            # 1, 2, 3 — elegir opción de respuesta
            if event.key == pygame.K_1:
                for npc in self.npcs:
                    npc.elegir_opcion(0)
            if event.key == pygame.K_2:
                for npc in self.npcs:
                    npc.elegir_opcion(1)
            if event.key == pygame.K_3:
                for npc in self.npcs:
                    npc.elegir_opcion(2)

    def update(self, dt):
        #si el inventario esta abierto se pausa el juego
        if self.inventario.visible:
            return
        old_x = self.player.x
        old_y = self.player.y

        self.player.update(dt)

        # Colisión con NPCs
        for npc in self.npcs:
            if self.player.rect.colliderect(npc.rect):
                self.player.x = old_x
                self.player.y = old_y
                self.player.rect.topleft = (int(old_x), int(old_y))

        # Colisión con entorno
        for obstaculo in self.obstaculos:
            if self.player.rect.colliderect(obstaculo):
                self.player.x = old_x
                self.player.y = old_y
                self.player.rect.topleft = (int(old_x), int(old_y))

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for npc in self.npcs:
            npc.draw(self.screen)

        self.player.draw(self.screen)
        self.inventario.draw(self.screen)

        # ── DEBUG: ver rectángulos de colisión ──
        # for obstaculo in self.obstaculos:
        #     pygame.draw.rect(self.screen, (255, 0, 0), obstaculo, 2)
        # pygame.draw.rect(self.screen, (0, 255, 0), self.player.rect, 2)
        # for npc in self.npcs:
        #     pygame.draw.rect(self.screen, (0, 0, 255), npc.rect, 2)