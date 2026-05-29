import pygame
import sys

class MenuScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        self.ANCHO = 800
        self.ALTO = 600

        # Paleta medieval — negro y dorado
        self.COLOR_FONDO       = (0, 0, 0)
        self.COLOR_ORO         = (201, 161, 74)
        self.COLOR_ORO_OPACO   = (100, 80, 40)
        self.COLOR_BORDE       = (60, 50, 30)

        self.fuente_titulo   = pygame.font.SysFont("Georgia", 52, bold=False)
        self.fuente_opciones = pygame.font.SysFont("Georgia", 22, bold=False)
        self.fuente_subtitulo = pygame.font.SysFont("Arial", 11)
        self.fuente_footer   = pygame.font.SysFont("Arial", 11)
        self.font_msg        = pygame.font.SysFont("Georgia", 20)

        self.opciones = ["Empezar", "Salir"]
        self.opcion_seleccionada = 0

        self.mostrando_intro = False
        self.mensaje_timer = 0
        self.duracion_intro = 5.0

        pygame.mixer.music.load("assets/sounds/menu.mp3")
        pygame.mixer.music.play(-1)

    def _opcion_rect(self, i):
        ancho_item = 220
        alto_item = 44
        x = self.ANCHO // 2 - ancho_item // 2
        y = self.ALTO // 2 + 20 + i * 56
        return pygame.Rect(x, y, ancho_item, alto_item)

    def handle_event(self, evento):
        if self.mostrando_intro:
            return

        if evento.type == pygame.MOUSEMOTION:
            for i in range(len(self.opciones)):
                if self._opcion_rect(i).collidepoint(evento.pos):
                    self.opcion_seleccionada = i

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i in range(len(self.opciones)):
                if self._opcion_rect(i).collidepoint(evento.pos):
                    self._confirmar(i)

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
            if evento.key == pygame.K_DOWN:
                self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
            if evento.key == pygame.K_RETURN:
                self._confirmar(self.opcion_seleccionada)

    def _confirmar(self, i):
        if self.opciones[i] == "Empezar":
            self.mostrando_intro = True
            self.mensaje_timer = 0
        elif self.opciones[i] == "Salir":
            pygame.quit()
            sys.exit()

    def update(self, dt):
        if self.mostrando_intro:
            self.mensaje_timer += dt
            if self.mensaje_timer >= self.duracion_intro:
                pygame.mixer.music.stop()
                from scenes.tavern import TavernScene
                self.game.change_scene(TavernScene(self.game))
                self.mostrando_intro = False
                return

    def draw(self):
        self.screen.fill(self.COLOR_FONDO)

        # ── Pantalla de intro ──
        if self.mostrando_intro:
            progreso = self.mensaje_timer / self.duracion_intro
            if progreso < 0.3:
                alpha = int((progreso / 0.3) * 255)
            elif progreso > 0.7:
                alpha = int(((1 - progreso) / 0.3) * 255)
            else:
                alpha = 255

            sup = self.font_msg.render(
                "Honor Knight  —  By Jacinto Cortez  —  2026",
                True, self.COLOR_ORO
            )
            sup.set_alpha(alpha)
            self.screen.blit(sup, (
                self.ANCHO // 2 - sup.get_width() // 2,
                self.ALTO // 2 - sup.get_height() // 2
            ))
            return

        # ── Esquinas decorativas ──
        tam = 18
        for (cx, cy, dx, dy) in [
            (20, 20, 1, 1), (self.ANCHO - 20, 20, -1, 1),
            (20, self.ALTO - 20, 1, -1), (self.ANCHO - 20, self.ALTO - 20, -1, -1)
        ]:
            pygame.draw.line(self.screen, self.COLOR_BORDE,
                             (cx, cy), (cx + dx * tam, cy), 1)
            pygame.draw.line(self.screen, self.COLOR_BORDE,
                             (cx, cy), (cx, cy + dy * tam), 1)

        # ── Título ──
        titulo = self.fuente_titulo.render("HONOR KNIGHT", True, self.COLOR_ORO)
        self.screen.blit(titulo, (
            self.ANCHO // 2 - titulo.get_width() // 2,
            self.ALTO // 2 - 130
        ))

        # Línea decorativa
        pygame.draw.line(self.screen, self.COLOR_BORDE,
                         (self.ANCHO // 2 - 100, self.ALTO // 2 - 82),
                         (self.ANCHO // 2 + 100, self.ALTO // 2 - 82), 1)

        # Subtítulo
        sub = self.fuente_subtitulo.render(
            "BY  JACINTO  CORTEZ     ·     2025",
            True, self.COLOR_BORDE
        )
        self.screen.blit(sub, (
            self.ANCHO // 2 - sub.get_width() // 2,
            self.ALTO // 2 - 70
        ))

        # ── Opciones ──
        for i, opcion in enumerate(self.opciones):
            rect = self._opcion_rect(i)
            activo = (i == self.opcion_seleccionada)

            if activo:
                hover_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                hover_surf.fill((201, 161, 74, 25))
                self.screen.blit(hover_surf, rect.topleft)

            color_label = self.COLOR_ORO if activo else self.COLOR_ORO_OPACO

            if activo:
                sym = self.fuente_opciones.render("✦", True, self.COLOR_ORO)
                self.screen.blit(sym, (rect.x + 10, rect.y + 10))
                self.screen.blit(sym, (rect.right - 30, rect.y + 10))

            texto = self.fuente_opciones.render(opcion.upper(), True, color_label)
            self.screen.blit(texto, (
                self.ANCHO // 2 - texto.get_width() // 2,
                rect.y + rect.height // 2 - texto.get_height() // 2
            ))

        # ── Footer ──
        footer = self.fuente_footer.render(
            "↑ ↓  navegar     Enter / clic  confirmar",
            True, self.COLOR_BORDE
        )
        self.screen.blit(footer, (
            self.ANCHO // 2 - footer.get_width() // 2,
            self.ALTO - 28
        ))