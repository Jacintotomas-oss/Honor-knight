import pygame
from mecanicas.Player import Player
from mecanicas.npc import NPC
from mecanicas.tavernero import Tavernero
from mecanicas.wallet import Wallet
from mecanicas.inventario import Inventario
from mecanicas.status import Status

#carga el fondo del patio de la taberna
class TavernYardScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.player = Player(100, 100)#esto carga al jugador junto con su sprite sheet y su sprite idle, ademas de configurar su animacion y su caja de colisiones
        self.wallet = Wallet(creditos_iniciales=1000)
        self.inventario = Inventario(self.wallet)
        self.status = Status(max_health=100)

        # NPCs con wallet conectado
        self.npcs = [
            NPC(590, 340, "bardo", wallet=self.wallet),
            Tavernero(wallet=self.wallet)
        ]

        

        # Cargar la imagen de fondo del patio de la taberna
        self.background = pygame.image.load("assets/backgrounds/tavern_Yard.png").convert()
        #musica del fondo
        #pygame.mixer.music.load("assets/sounds/t1.mp3")
        
        #posicion incial del jugador en el patio de la taberna
        self.player.x = 200
        self.player.y = 260

        #colisiones del entorno
        self.obstaculos = [
            pygame.Rect(11, 18, 998, 111),  # zona 1
            pygame.Rect(313, 207, 367, 69),  # zona 2
            pygame.Rect(49, 207, 127, 67),  # zona 3
            pygame.Rect(856, 198, 142, 71),  # zona 4
            pygame.Rect(51, 707, 80, 47),  # zona 5
            pygame.Rect(838, 707, 151, 49),  # zona 6
            pygame.Rect(329, 733, 293, 38),  # zona 7
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
        # Colisiones con obstáculos
        for obstacul in self.obstaculos:
            if self.player.rect.colliderect(obstacul):
                    self.player.x = old_x
                    self.player.y = old_y
                    self.player.rect.topleft = (int(old_x), int(old_y))
        #cambio de escena 
        if self.player.y > 500:
            from scenes.yard import YardScene
            self.game.change_scene(YardScene(self.game))
        #regresar a la escena anterior
        if self.player.x < -50:
            from scenes.tavern import TavernScene
            self.game.change_scene(TavernScene(self.game))
            #posicion del jugador al regresar a la taberna
            self.player.x = 750
            self.player.y = 250
    def draw(self):
            self.screen.blit(self.background, (0, 0))

            # Primero todos los sprites
            #los npc no se cargaran en esta escena
            #for npc in self.npcs:
             #   npc.draw(self.screen)
            self.player.draw(self.screen)

            # Luego las burbujas encima de todo
            #for npc in self.npcs:
             #   npc.draw_burbuja(self.screen)

            self.inventario.draw(self.screen)
            self.status.draw(self.screen)

            #for obstaculo in self.obstaculos:
             #   pygame.draw.rect(self.screen, (255, 0, 0), obstaculo, 2)
              #  pygame.draw.rect(self.screen, (0, 255, 0), self.player.rect, 2)
                #for npc in self.npcs:
                 #   pygame.draw.rect(self.screen, (0, 0, 255), npc.rect, 2)


