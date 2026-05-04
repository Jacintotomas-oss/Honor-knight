import pygame
from mecanicas.Player import Player
from mecanicas.npc import NPC
from mecanicas.tavernero import Tavernero
from mecanicas.wallet import Wallet
from mecanicas.inventario import Inventario
from mecanicas.status import Status

class TavernScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.player = Player(100, 100)
        self.wallet = Wallet(creditos_iniciales=1000)
        self.inventario = Inventario(self.wallet)
        self.status = Status(max_health=100)

        # NPCs con wallet conectado
        self.npcs = [
            NPC(590, 340, "bardo", wallet=self.wallet),
            Tavernero(wallet=self.wallet)
        ]

        # Cargar la imagen de fondo de la taberna
        self.background = pygame.image.load("assets/backgrounds/tavern.png").convert()
        #musica del fondo 
        pygame.mixer.music.load("assets/sounds/t1.mp3")
        pygame.mixer.music.play(-1)
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

            # Abrir/cerrar inventario
            if event.key == pygame.K_i:
                self.inventario.toggle()
                return

            if self.inventario.visible:
                return

            # E — activar diálogo, confirmar propina o cerrar respuesta
            if event.key == pygame.K_e:
                for npc in self.npcs:
                    distancia = abs(npc.rect.centerx - self.player.rect.centerx) + \
                                abs(npc.rect.centery - self.player.rect.centery)
                    if distancia < 150:
                        if npc.modo_propina:
                            npc.confirmar_propina()
                        elif npc.respuesta_activa:
                            npc.cerrar_respuesta()
                        else:
                            npc.activar()

            # R — cerrar diálogo o saltar propina
            if event.key == pygame.K_r:
                for npc in self.npcs:
                    if npc.modo_propina:
                        npc.saltar_propina()
                    else:
                        npc._resetear()

            # Flechas — ajustar propina
            if event.key == pygame.K_UP:
                for npc in self.npcs:
                    if npc.modo_propina:
                        npc.ajustar_propina("arriba")

            if event.key == pygame.K_DOWN:
                for npc in self.npcs:
                    if npc.modo_propina:
                        npc.ajustar_propina("abajo")

            # 1, 2, 3, 4 — elegir opción de respuesta
            if event.key == pygame.K_1:
                for npc in self.npcs:
                    npc.elegir_opcion(0)
            if event.key == pygame.K_2:
                for npc in self.npcs:
                    npc.elegir_opcion(1)
            if event.key == pygame.K_3:
                for npc in self.npcs:
                    npc.elegir_opcion(2)
            if event.key == pygame.K_4:
                for npc in self.npcs:
                    npc.elegir_opcion(3)
                    #mostrar el inventario al presionar i
            if event.key == pygame.K_i:
                self.inventario.toggle()
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                self.status.toggle()
                return


    def update(self, dt):
        if self.inventario.visible:
            return

        old_x = self.player.x
        old_y = self.player.y

        self.player.update(dt)
        self.status.update(dt)

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

            # Primero todos los sprites
            for npc in self.npcs:
                npc.draw(self.screen)
            self.player.draw(self.screen)

            # Luego las burbujas encima de todo
            for npc in self.npcs:
                npc.draw_burbuja(self.screen)

            self.inventario.draw(self.screen)
            self.status.draw(self.screen)

        # ── DEBUG: ver rectángulos de colisión ──
        # for obstaculo in self.obstaculos:
        #     pygame.draw.rect(self.screen, (255, 0, 0), obstaculo, 2)
        # pygame.draw.rect(self.screen, (0, 255, 0), self.player.rect, 2)
        # for npc in self.npcs:
        #     pygame.draw.rect(self.screen, (0, 0, 255), npc.rect, 2)