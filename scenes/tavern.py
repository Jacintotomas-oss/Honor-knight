import pygame
from mecanicas.Player import Player
from mecanicas.npc import NPC

class TavernScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.player = Player(100, 100)

        # NPC estático del bardo en la taberna
        self.npcs = [
            NPC(590, 340)  # bardo cerca de la barra
        ]

        # Cargar la imagen de fondo de la taberna
        self.background = pygame.image.load("assets/backgrounds/tavern.png").convert()

        # Rectángulos de colisión del entorno
        self.obstaculos = [
                        #98 esquina superior izquierda, 283 esquina superior derecha, 203 ancho, 142 alto
            pygame.Rect(98, 283, 190, 112),  # zona 1 )
            pygame.Rect(282, 529, 175, 130),  # zona 2
            pygame.Rect(514, 276, 412, 24),  # zona 3 barra
            pygame.Rect(769, 61, 230, 145),  # zona 4
            pygame.Rect(471, 82, 287, 25),  # zona 5
            pygame.Rect(790, 451, 68, 399),
            pygame.Rect(61, 77, 698, 15),
    ]

    def handle_event(self, event):
        pass

    def update(self, dt):
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

        # ── DEBUG: ver rectángulos de colisión ──
        # Quita estas líneas cuando ya estén bien posicionados
        #for obstaculo in self.obstaculos:
         #   pygame.draw.rect(self.screen, (255, 0, 0), obstaculo, 2)
        #pygame.draw.rect(self.screen, (0, 255, 0), self.player.rect, 2)
        #for npc in self.npcs:
         #   pygame.draw.rect(self.screen, (0, 0, 255), npc.rect, 2)