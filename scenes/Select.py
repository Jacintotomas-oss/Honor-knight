import pygame 
import sys

class Select_Option:
    def __init__(self,game):
        self.game = game
        self.screen = game.screen

        self.ANCHO = 800
        self.ALTO = 600
        self.Color_Fondo = (0,0,0)
        self.COLOR_ORO  = (201, 161, 74)

        self.fuente_titulo   = pygame.font.SysFont("Georgia", 52, bold=False)
        self.fuente_opciones = pygame.font.SysFont("Georgia", 22, bold=False)
        self.fuente_subtitulo = pygame.font.SysFont("Arial", 11)
        self.fuente_footer   = pygame.font.SysFont("Arial", 11)
        self.font_msg        = pygame.font.SysFont("Georgia", 20)

        self.opciones = ["Empezar Capitulo 1","Cargar Partida","juego libre","Regresar"]
        self.opcion_seleccionada = 0

        self.mostrando_intro = False
        self.mensaje_timer = 0
        self.duracion_intro = 25.0

    def _opcion_rect(self, i):
        ancho_item = 220
        alto_item = 44

        x = self.ANCHO // 2 - ancho_item //2
        y = self.ALTO // 2+20 + i * 56
        return pygame.Rect(x,y, ancho_item, alto_item)

    def handle_event(self, event):
        if self.mostrando_intro:
            return
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
        #mostrar mensajes
        if self.mostrando_intro:
            progreso = self.mensaje_timer/self.duracion_intro
            if progreso < 0.3:
                alpha = int((progreso / 0.3)*255)
            elif progreso > 0.7:
                alpha = int(((1 - progreso) / 0.3)*255)
            else:
                alpha = 255
            
            sup =self.font_msg.render(

                "Mas alla del Mar del norte - invierno - 320",
                True, self.COLOR_ORO
                
            )

        
           

            sup.set_alpha(alpha)
            self.screen.blit(sup, (
                self.ANCHO // 2 - sup.get_width() // 2,
                self.ALTO // 2 - sup.get_height() // 2
            ))
            return


        # --- Título ---
        titulo_surf = self.fuente_titulo.render("Seleccionar Opción", True, (255, 255, 255))
        titulo_rect = titulo_surf.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 - 80))
        self.screen.blit(titulo_surf, titulo_rect)

        # --- Opciones del menú ---
        for i, opcion in enumerate(self.opciones):
            rect = self._opcion_rect(i)

            # Resaltar la opción seleccionada
            if i == self.opcion_seleccionada:
                pygame.draw.rect(self.screen, (70, 70, 70), rect, border_radius=8)  # fondo gris
                color_texto = (255, 215, 0)   # dorado
            else:
                color_texto = (200, 200, 200) # gris claro

            # Dibujar borde del rectángulo
            pygame.draw.rect(self.screen, (150, 150, 150), rect, width=1, border_radius=8)

            # Renderizar texto centrado en el rect
            texto_surf = self.fuente_opciones.render(opcion, True, color_texto)
            texto_rect = texto_surf.get_rect(center=rect.center)
            self.screen.blit(texto_surf, texto_rect)

        pygame.display.flip()  # ← importante: actualiza la pantalla
            

    def update(self, dt):
        if self.mostrando_intro:
            self.mensaje_timer += dt
            if self.mensaje_timer >= self.duracion_intro:
                from scenes.Cap1 import Cap1
                self.game.change_scene(Cap1(self.game)) 
                pygame.mixer.music.stop()


    def _confirmar(self,i):
        if self.opciones[i] == "Empezar Capitulo 1":
            self.mostrando_intro = True
            self.mensaje_timer = 0
            #cambio de escena
                       
        elif self.opciones[i] == "Cargar Partida":
            pass

        elif self.opciones[i] == "juego libre":
              self.mostrando_intro = True
              self.mensaje_timer = 0
        elif self.opciones[i]== "Regresar":
            #volver a la escena anterior
            from scenes.Act1 import Act1Scene
            self.game.change_scene(Act1Scene(self.game))






    