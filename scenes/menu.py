import pygame
import sys

class MenuScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        self.ANCHO = 800
        self.ALTO = 600

        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)

        self.fuente = pygame.font.Font(None, 50)
        self.font_msg = pygame.font.Font(None, 30)
        self.opciones = ["Empezar", "Salir"]
        self.opcion_seleccionada = 0

        # Estado de la pantalla de introducción
        self.mostrando_intro = False
        self.mensaje_timer = 0
        self.duracion_intro = 5.0  # segundos que dura la intro

        # Música del menú
        pygame.mixer.music.load("assets/sounds/menu.mp3")
        pygame.mixer.music.play(-1)

    def handle_event(self, evento):
        if self.mostrando_intro:
            return  # bloquea input durante la intro

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_UP:
                self.opcion_seleccionada -= 1
                if self.opcion_seleccionada < 0:
                    self.opcion_seleccionada = len(self.opciones) - 1

            if evento.key == pygame.K_DOWN:
                self.opcion_seleccionada += 1
                if self.opcion_seleccionada >= len(self.opciones):
                    self.opcion_seleccionada = 0

            if evento.key == pygame.K_RETURN:
                if self.opciones[self.opcion_seleccionada] == "Empezar":
                    self.mostrando_intro = True
                    self.mensaje_timer = 0

                if self.opciones[self.opcion_seleccionada] == "Salir":
                    pygame.quit()
                    sys.exit()

    def update(self, dt):
        if self.mostrando_intro:
            self.mensaje_timer += dt
            if self.mensaje_timer >= self.duracion_intro:
                # Termina la intro y cambia a la taberna
                pygame.mixer.music.stop()
                from scenes.tavern import TavernScene
                self.game.change_scene(TavernScene(self.game))

    def draw(self):
        self.screen.fill(self.NEGRO)

        if self.mostrando_intro:
            # Fondo negro con fade in/out del texto
            progreso = self.mensaje_timer / self.duracion_intro
            if progreso < 0.3:
                alpha = int((progreso / 0.3) * 255)   # fade in
            elif progreso > 0.7:
                alpha = int(((1 - progreso) / 0.3) * 255)  # fade out
            else:
                alpha = 255  # visible completo

            superficie = self.font_msg.render(
                "Honor Knight  —  By Jacinto Cortez  —  2025",
                True, (255, 255, 255)

            #mostrar otro fondo negro indicando la fecha y el lugar de la taverna
             
            )
            superficie.set_alpha(alpha)
            self.screen.blit(
                superficie,
                (self.ANCHO // 2 - superficie.get_width() // 2,
                 self.ALTO // 2 - superficie.get_height() // 2)
            )
            return

        # Menú normal
        for i, opcion in enumerate(self.opciones):
            color = self.BLANCO if i == self.opcion_seleccionada else (150, 150, 150)
            texto = self.fuente.render(opcion, True, color)
            rect = texto.get_rect()
            rect.centerx = self.ANCHO // 2
            rect.centery = self.ALTO // 2 + i * 60
            self.screen.blit(texto, rect)
