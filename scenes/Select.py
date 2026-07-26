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

        self.opciones = ["Empezar Capitulo 1","juego libre","Regresar"]
        self.opcion_seleccionada = 0

        self.mostrando_intro = False
        self.mensaje_timer = 0
        self.duracion_intro = 25.0

        self.mostrando_audio = False
        self.audio_timer = 0.0
        self.audio_duracion = 20.0

        # Estado para el mensaje "Muy pronto"
        self.mostrando_muy_pronto = False
        self.muy_pronto_timer = 0.0
        self.muy_pronto_duracion = 3.0

        self.cap1_precargado = None

    def _opcion_rect(self, i):
        ancho_item = 220
        alto_item = 44
        x = self.ANCHO // 2 - ancho_item //2
        y = self.ALTO // 2+20 + i * 56
        return pygame.Rect(x,y, ancho_item, alto_item)

    def handle_event(self, event):
        if self.mostrando_intro or self.mostrando_audio or self.mostrando_muy_pronto:
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

        if self.mostrando_intro:
            progreso = self.mensaje_timer/self.duracion_intro
            if progreso < 0.3:
                alpha = int((progreso / 0.3)*255)
            elif progreso > 0.7:
                alpha = int(((1 - progreso) / 0.3)*255)
            else:
                alpha = 255
            sup = self.font_msg.render(
                "Mas alla del Mar del norte - invierno - 320",
                True, self.COLOR_ORO
            )
            sup.set_alpha(alpha)
            self.screen.blit(sup, (
                self.ANCHO // 2 - sup.get_width() // 2,
                self.ALTO // 2 - sup.get_height() // 2
            ))
            return

        if self.mostrando_audio:
            return

        # Mensaje "Muy pronto"
        if self.mostrando_muy_pronto:
            texto = self.font_msg.render("Muy pronto...", True, self.COLOR_ORO)
            self.screen.blit(texto, (
                self.ANCHO // 2 - texto.get_width() // 2,
                self.ALTO // 2 - texto.get_height() // 2
            ))
            return

        # --- Título ---
        titulo_surf = self.fuente_titulo.render("Seleccionar Opción", True, (255, 255, 255))
        titulo_rect = titulo_surf.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 - 80))
        self.screen.blit(titulo_surf, titulo_rect)

        # --- Opciones del menú ---
        for i, opcion in enumerate(self.opciones):
            rect = self._opcion_rect(i)
            if i == self.opcion_seleccionada:
                pygame.draw.rect(self.screen, (70, 70, 70), rect, border_radius=8)
                color_texto = (255, 215, 0)
            else:
                color_texto = (200, 200, 200)
            pygame.draw.rect(self.screen, (150, 150, 150), rect, width=1, border_radius=8)
            texto_surf = self.fuente_opciones.render(opcion, True, color_texto)
            texto_rect = texto_surf.get_rect(center=rect.center)
            self.screen.blit(texto_surf, texto_rect)

        pygame.display.flip()

    def update(self, dt):
        if self.mostrando_intro:
            self.mensaje_timer += dt
            if self.mensaje_timer >= self.duracion_intro:
                self.mostrando_intro = False
                self.mostrando_audio = True
                self.audio_timer = 0
                pygame.mixer.music.load("assets/sounds/prologo.mp3")
                pygame.mixer.music.play()

        if self.mostrando_audio and self.cap1_precargado is None:
            from scenes.Cap1 import Cap1
            self.cap1_precargado = Cap1(self.game)

        if self.mostrando_audio:
            self.audio_timer += dt
            if self.audio_timer >= self.audio_duracion:
                pygame.mixer.music.stop()
                self.game.change_scene(self.cap1_precargado)
                self.cap1_precargado.iniciar_musica()
                    

        # Timer del mensaje "Muy pronto"
        if self.mostrando_muy_pronto:
            self.muy_pronto_timer += dt
            if self.muy_pronto_timer >= self.muy_pronto_duracion:
                self.mostrando_muy_pronto = False
                self.muy_pronto_timer = 0.0

    def _confirmar(self, i):
        if self.opciones[i] == "Empezar Capitulo 1":
            self.mostrando_intro = True
            self.mensaje_timer = 0
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.stop()

        elif self.opciones[i] == "juego libre":
            self.mostrando_muy_pronto = True
            self.muy_pronto_timer = 0.0

        elif self.opciones[i] == "Regresar":
            from scenes.Act1 import Act1Scene
            self.game.change_scene(Act1Scene(self.game))