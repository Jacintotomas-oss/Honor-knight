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
            if event.key == pygame.K_i:
                self.inventario.toggle()
                return
            if self.inventario.visible:
                return
            if event.key == pygame.K_LSHIFT:
                self.status.toggle()
                return
            if event.key == pygame.K_e:
                for npc in self.women_npcs:
                    distancia = abs(npc.rect.centerx - self.player.rect.centerx) + \
                                abs(npc.rect.centery - self.player.rect.centery)
                    if distancia < 300:
                        if npc.modo_propina:
                            npc.confirmar_propina()
                        elif npc.respuesta_activa:
                            npc.cerrar_respuesta()
                        else:
                            npc.activar()
            if event.key == pygame.K_r:
                for npc in self.women_npcs:
                    if npc.modo_propina:
                        npc.saltar_propina()
                    else:
                        npc._resetear()
            if event.key == pygame.K_UP:
                for npc in self.women_npcs:
                    if npc.modo_propina:
                        npc.ajustar_propina("arriba")
            if event.key == pygame.K_DOWN:
                for npc in self.women_npcs:
                    if npc.modo_propina:
                        npc.ajustar_propina("abajo")
            if event.key == pygame.K_1:
                for npc in self.women_npcs:
                    npc.elegir_opcion(0)
            if event.key == pygame.K_2:
                for npc in self.women_npcs:
                    npc.elegir_opcion(1)
            if event.key == pygame.K_3:
                for npc in self.women_npcs:
                    npc.elegir_opcion(2)
            if event.key == pygame.K_4:
                for npc in self.women_npcs:
                    npc.elegir_opcion(3)
         

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

        #burbujas de dialogo
        for npc in self.women_npcs:
            npc.draw_burbuja(self.screen)

        #burbujas
        for npc in self.npcs:
            npc.draw_burbuja(self.screen)

       # for obstaculo in self.obstaculos:
        #    pygame.draw.rect(self.screen, (255, 0, 0), obstaculo, 2)
         #   pygame.draw.rect(self.screen, (0, 255, 0), self.player.rect, 2)
            #for npc in self.npcs:
             #       pygame.draw.rect(self.screen, (0, 0, 255), npc.rect, 2)
          #  for woman_npc in self.women_npcs:
           #         pygame.draw.rect(self.screen, (255, 0, 255), woman_npc.rect, 2)
