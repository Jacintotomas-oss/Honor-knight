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
        self.opciones = ["Empezar", "Salir"]
        self.opcion_seleccionada = 0

    def handle_event(self, evento):
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
                    from scenes.tavern import TavernScene
                    self.game.change_scene(TavernScene(self.game))

                if self.opciones[self.opcion_seleccionada] == "Salir":
                    pygame.quit()
                    sys.exit()

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill(self.NEGRO)

        for i, opcion in enumerate(self.opciones):
            color = self.BLANCO if i == self.opcion_seleccionada else (150, 150, 150)
            texto = self.fuente.render(opcion, True, color)
            rect = texto.get_rect()
            rect.centerx = self.ANCHO // 2
            rect.centery = self.ALTO // 2 + i * 60
            self.screen.blit(texto, rect)
