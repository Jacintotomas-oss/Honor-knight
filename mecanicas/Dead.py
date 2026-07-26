import pygame
from mecanicas.inventario import Inventario
from mecanicas.status import Status
from mecanicas.Player import Player

class Dead (Player, Status):
    def __init__(self, x, y, ):
        super().__init__(x, y)
        
        #setear atributos de Status
        self.max_health = 100
        self.alive = False
        #stats 
        self.higiene = 0.0
        self.hambre = 0.0
        self.sed = 0.0
        self.herida = True
        self.infectado = True
        self.enfermedad = "Muerte"

        #tiempo de acumulado en segundos se usara en condicional 
        self.tiempo_total = 0.0

        self.face = 0 
        # 0=recién muerto, 1=temprana, 2=avanzada, 3=restos

        self.radio_olor = 150
        self.rect = pygame.Rect(x, y, 32, 32)
    
    def update(self, dt):
        self.tiempo_total += dt

        if self.tiempo_total < 86400:
            self.face = 0
            #de 86400 a 259200 fase 1
        elif self.tiempo_total < 259200:
            self.face = 1
            #de 259200 a 604800 fase 2
        elif self.tiempo_total < 604800:
            self.face = 2
        else:
            self.face = 3

    def verificar_proximidad(self, player_rect, status_jugador):
        distancia = abs(self.rect.centerx - player_rect.centerx) + \
                    abs(self.rect.centery - player_rect.centery)
        
        if distancia <= self.radio_olor:
            if self.face == 0:
                status_jugador.higiene -= 0.1
            elif self.face == 1:
                status_jugador.higiene -= 0.2
            elif self.face == 2:
                status_jugador.higiene -= 0.3
            elif self.face == 3:
                status_jugador.higiene -= 0.0 #son restos, no huele

    def draw(self, screen):
        if self.face == 0:
            color = (180, 170, 160)  # gris pálido      # azul
        elif self.face == 1:
            color = (100, 120, 80)  # verde grisáceo     # verde oscuro
        elif self.face == 2:
            color = (60, 40, 20)  # marrón muy oscuro    # marrón
        else:
            color = (200, 180, 120)  # beige amarillento          # gris

        pygame.draw.rect(screen, color, self.rect, 2)