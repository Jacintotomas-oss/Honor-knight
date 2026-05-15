import pygame 
import sys

class Select_Option:
    def __init__(self,game):
        self.game = game
        self.screen = game.screen

        self.ANCHO = 800
        self.ALTO = 600
        self.Color_Fondo = (0,0,0)

        self.fuente_titulo   = pygame.font.SysFont("Georgia", 52, bold=False)
        self.fuente_opciones = pygame.font.SysFont("Georgia", 22, bold=False)
        self.fuente_subtitulo = pygame.font.SysFont("Arial", 11)
        self.fuente_footer   = pygame.font.SysFont("Arial", 11)
        self.font_msg        = pygame.font.SysFont("Georgia", 20)

        self.opciones = ["Empezar Capitulo 1","Cargar Partida","juego libre","Regresar"]
        self.opcion_seleccionada = 0

    def _opcion_rect(self, i):
        ancho_item = 220
        alto_item = 44

        x = self.ANCHO // 2 - ancho_item //2
        y = self.ALTO // 2+20 + i * 56
        return pygame.Rect(x,y, ancho_item, alto_item)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            for i in range(len(self.opciones)):
                if self._opcion_rect(i).collidepoint(event.pos):
                    self.opcion_seleccionada = i

        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
            for i in range(len(self.opciones)):
                if self._opcion_rect(i).collidepoint(event.pos):
                    self._confirmar(i)

    def draw(self):
        self.screen.fill(self.Color_Fondo)

    def update(self, dt):
        pass

    def _confirmar(self,i):
        if self.opciones[i] == "Empezar Capitulo 1":
            #cambio de escena
            from scenes.Cap1 import Cap1
            self.game.change_scene(Cap1(self.game))             
        elif self.opciones[i] == "Cargar Partida":
            pass

        elif self.opciones[i] == "juego libre":
            pass
        elif self.opciones[i]== "Regresar":
            pass






    