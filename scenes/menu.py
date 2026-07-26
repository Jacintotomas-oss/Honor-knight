import pygame
import sys
import math
import random


class MenuScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        self.ANCHO = 800
        self.ALTO = 600

        # ── Paleta "Luna de Sangre" ──────────────────────────────
        self.COLOR_TEXTO       = (228, 228, 238)
        self.COLOR_TEXTO_OPACO = (120, 122, 140)
        self.COLOR_ACENTO      = (205, 45, 58)
        self.COLOR_ACENTO_OSC  = (110, 20, 28)
        self.COLOR_SOMBRA_TXT  = (10, 8, 14)

        # Fuentes — pixel art auténtico
        try:
            self.fuente_titulo    = pygame.font.Font("assets/fonts/PressStart2P.ttf", 26)
            self.fuente_opciones  = pygame.font.Font("assets/fonts/PressStart2P.ttf", 11)
            self.fuente_subtitulo = pygame.font.Font("assets/fonts/PressStart2P.ttf", 7)
            self.fuente_footer    = pygame.font.Font("assets/fonts/PressStart2P.ttf", 6)
            self.font_msg         = pygame.font.Font("assets/fonts/PressStart2P.ttf", 9)
        except FileNotFoundError:
            self.fuente_titulo    = pygame.font.SysFont("Courier New", 32, bold=True)
            self.fuente_opciones  = pygame.font.SysFont("Courier New", 16, bold=True)
            self.fuente_subtitulo = pygame.font.SysFont("Courier New", 10)
            self.fuente_footer    = pygame.font.SysFont("Courier New", 10)
            self.font_msg         = pygame.font.SysFont("Courier New", 13)

        self.opciones = ["Empezar", "Salir"]
        self.opcion_seleccionada = 0

        self.mostrando_intro = False
        self.mensaje_timer = 0
        self.duracion_intro = 5.0

        self.blink_timer = 0.0
        self.blink_visible = True

        # Geometría de la luna (misma composición que la portada)
        self.luna_cx = self.ANCHO // 2
        self.luna_cy = 232
        self.luna_r = 108

        # El fondo es estático → se construye UNA vez y se cachea
        self.fondo = self._construir_fondo()

        pygame.mixer.music.load("assets/sounds/menu.mp3")
        pygame.mixer.music.play(-1)

    def _opcion_rect(self, i):
        ancho_item = 220
        alto_item = 44
        x = self.ANCHO // 2 - ancho_item // 2
        y = 402 + i * 60
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

        self.blink_timer += dt
        if self.blink_timer >= 0.5:
            self.blink_timer = 0.0
            self.blink_visible = not self.blink_visible

    # ── Utilidades de color ──────────────────────────────────────

    @staticmethod
    def _lerp_color(c1, c2, t):
        t = max(0.0, min(1.0, t))
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
        )

    # ── Construcción del fondo (una sola vez) ────────────────────

    def _construir_fondo(self):
        surf = pygame.Surface((self.ANCHO, self.ALTO))
        self._dibujar_cielo(surf)
        self._dibujar_facetas_cielo(surf)
        self._dibujar_terreno(surf)
        self._dibujar_estrellas(surf)
        self._dibujar_halo(surf, self.luna_cx, self.luna_cy, self.luna_r)
        self._dibujar_gotas_sangre(surf, self.luna_cx, self.luna_cy, self.luna_r)
        self._dibujar_luna_facetada(surf, self.luna_cx, self.luna_cy, self.luna_r)
        return surf

    def _dibujar_cielo(self, surf):
        arriba = (14, 17, 30)
        abajo = (76, 88, 108)
        for y in range(self.ALTO):
            t = y / self.ALTO
            color = self._lerp_color(arriba, abajo, t)
            pygame.draw.line(surf, color, (0, y), (self.ANCHO, y))

    def _dibujar_facetas_cielo(self, surf):
        # Grandes planos diagonales, estilo low-poly, como la portada
        facetas = [
            ([(0, 0), (520, 0), (260, 210), (0, 260)], (22, 26, 44), 60),
            ([(520, 0), (self.ANCHO, 0), (self.ANCHO, 140), (260, 210)], (34, 40, 60), 45),
            ([(0, 260), (260, 210), (self.ANCHO, 140), (self.ANCHO, 340), (0, 420)],
             (48, 56, 76), 55),
            ([(0, 420), (self.ANCHO, 340), (self.ANCHO, self.ALTO), (0, self.ALTO)],
             (64, 74, 94), 40),
            ([(self.ANCHO, 140), (self.ANCHO, self.ALTO), (620, self.ALTO), (self.ANCHO, 340)],
             (56, 66, 88), 35),
        ]
        for puntos, color, alpha in facetas:
            capa = pygame.Surface((self.ANCHO, self.ALTO), pygame.SRCALPHA)
            pygame.draw.polygon(capa, (*color, alpha), puntos)
            surf.blit(capa, (0, 0))

    def _dibujar_terreno(self, surf):
        y0 = self.ALTO - 132
        pygame.draw.polygon(
            surf, (16, 14, 20),
            [(0, y0 + 40), (self.ANCHO, y0), (self.ANCHO, self.ALTO), (0, self.ALTO)]
        )
        pygame.draw.polygon(
            surf, (32, 27, 36),
            [(0, y0 + 40), (self.ANCHO, y0), (self.ANCHO, y0 + 70), (0, y0 + 95)]
        )
        pygame.draw.polygon(
            surf, (44, 36, 48),
            [(0, y0 + 40), (330, y0 + 18), (280, y0 + 60), (0, y0 + 95)]
        )
        # línea de cresta que separa los dos tonos
        pygame.draw.line(surf, (58, 48, 62), (0, y0 + 40), (self.ANCHO, y0), 2)

    def _dibujar_estrellas(self, surf):
        rng = random.Random(11)
        zona_exclusion = (self.luna_cx, self.luna_cy, self.luna_r + 60)
        for _ in range(30):
            x = rng.randint(10, self.ANCHO - 10)
            y = rng.randint(10, self.ALTO - 150)
            dx, dy = x - zona_exclusion[0], y - zona_exclusion[1]
            if dx * dx + dy * dy < zona_exclusion[2] ** 2:
                continue
            size = rng.choice([1, 1, 1, 2])
            brillo = rng.randint(120, 190)
            pygame.draw.rect(surf, (brillo, brillo, brillo + 14), (x, y, size, size))

        for x, y, size in [(60, 90, 7), (700, 60, 5), (650, 250, 4), (110, 300, 4), (740, 400, 3)]:
            self._dibujar_estrella_chispa(surf, x, y, size, (170, 176, 196))

    def _dibujar_estrella_chispa(self, surf, x, y, size, color):
        pygame.draw.line(surf, color, (x - size, y), (x + size, y), 1)
        pygame.draw.line(surf, color, (x, y - size), (x, y + size), 1)
        s2 = max(1, size // 2)
        pygame.draw.line(surf, color, (x - s2, y - s2), (x + s2, y + s2), 1)
        pygame.draw.line(surf, color, (x - s2, y + s2), (x + s2, y - s2), 1)

    def _dibujar_halo(self, surf, cx, cy, r):
        capa = pygame.Surface((self.ANCHO, self.ALTO), pygame.SRCALPHA)
        for i, radio in enumerate(range(int(r * 2.6), r, -6)):
            alpha = int(4 + (i * 0.6))
            pygame.draw.circle(capa, (90, 70, 90, min(alpha, 70)), (cx, cy), radio)
        surf.blit(capa, (0, 0))

    # ── Luna facetada (low-poly, sombreada) ──────────────────────

    def _sombra_esfera(self, nx, ny):
        z = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
        luz = (-0.55, -0.65, 0.62)
        dot = nx * luz[0] + ny * luz[1] + z * luz[2]
        return max(0.42, min(1.0, dot))

    def _dibujar_luna_facetada(self, surf, cx, cy, r):
        rng = random.Random(77)
        oscuro = (150, 8, 14)
        claro = (255, 46, 46)

        def punto(nx, ny):
            return (cx + nx * r, cy + ny * r)

        def color_facet(pts_n):
            avgx = sum(p[0] for p in pts_n) / len(pts_n)
            avgy = sum(p[1] for p in pts_n) / len(pts_n)
            sombra = self._sombra_esfera(avgx, avgy)
            sombra += rng.uniform(-0.02, 0.02)
            base = self._lerp_color(oscuro, claro, sombra)
            return base

        def anillo(frac, seg, jitter_ang, jitter_rad):
            pts = []
            for i in range(seg):
                ang = 2 * math.pi * i / seg + rng.uniform(-jitter_ang, jitter_ang)
                rr = frac + rng.uniform(-jitter_rad, jitter_rad)
                pts.append((rr * math.cos(ang), rr * math.sin(ang)))
            return pts

        # Muy pocas facetas: solo un abanico central + un anillo exterior
        SEG = 7
        anillos_n = [
            anillo(0.58, SEG, 0.08, 0.02),
            anillo(1.02, SEG, 0.05, 0.02),
        ]
        centro_n = (0.0, 0.0)

        # Abanico central
        for i in range(SEG):
            j = (i + 1) % SEG
            tri_n = [centro_n, anillos_n[0][i], anillos_n[0][j]]
            tri_px = [punto(*p) for p in tri_n]
            color = color_facet([anillos_n[0][i], anillos_n[0][j]])
            pygame.draw.polygon(surf, color, tri_px)
            pygame.draw.polygon(surf, self._lerp_color(color, (0, 0, 0), 0.12), tri_px, 1)

        # Franja exterior
        for k in range(len(anillos_n) - 1):
            interior = anillos_n[k]
            exterior = anillos_n[k + 1]
            for i in range(SEG):
                j = (i + 1) % SEG
                a, b = interior[i], interior[j]
                c, d = exterior[j], exterior[i]
                for tri_n in ([a, b, c], [a, c, d]):
                    tri_px = [punto(*p) for p in tri_n]
                    color = color_facet(tri_n)
                    pygame.draw.polygon(surf, color, tri_px)
                    pygame.draw.polygon(surf, self._lerp_color(color, (0, 0, 0), 0.12), tri_px, 1)

    def _dibujar_gotas_sangre(self, surf, cx, cy, r):
        rng = random.Random(4)
        oscuro = (70, 10, 16)
        medio = (140, 22, 30)
        xs = [x for x in range(-int(r * 0.85), int(r * 0.85) + 1, int(r * 0.19))]
        for idx, dx in enumerate(xs):
            y0 = cy + math.sqrt(max(0.0, r * r - dx * dx)) - 4
            centralidad = 1 - abs(dx) / (r * 0.85 + 1)
            largo = r * (0.35 + centralidad * 1.7) * rng.uniform(0.75, 1.15)
            ancho = rng.uniform(5, 11)
            x0 = cx + dx
            punta_y = y0 + largo
            pygame.draw.polygon(surf, medio, [
                (x0 - ancho / 2, y0), (x0 + ancho / 2, y0), (x0, punta_y)
            ])
            if rng.random() < 0.4:
                gy = punta_y + rng.uniform(14, 34)
                gs = rng.uniform(3, 6)
                pygame.draw.polygon(surf, oscuro, [
                    (x0, gy - gs), (x0 + gs * 0.6, gy), (x0, gy + gs), (x0 - gs * 0.6, gy)
                ])

    # ── Panel translúcido para legibilidad de la UI ───────────────

    def _dibujar_panel_ui(self):
        capa = pygame.Surface((self.ANCHO, self.ALTO - 375), pygame.SRCALPHA)
        for y in range(capa.get_height()):
            t = y / capa.get_height()
            alpha = int(30 + t * 130)
            pygame.draw.line(capa, (6, 5, 10, alpha), (0, y), (self.ANCHO, y))
        self.screen.blit(capa, (0, 375))

    # ── Draw principal ─────────────────────────────────────────────

    def draw(self):
        self.screen.blit(self.fondo, (0, 0))

        if self.mostrando_intro:
            self.screen.fill((6, 5, 9))
            progreso = self.mensaje_timer / self.duracion_intro
            if progreso < 0.3:
                alpha = int((progreso / 0.3) * 255)
            elif progreso > 0.7:
                alpha = int(((1 - progreso) / 0.3) * 255)
            else:
                alpha = 255

            sup = self.font_msg.render(
                "Honor Knight  —  By Jacinto Cortez  —  2025",
                True, self.COLOR_TEXTO
            )
            sup.set_alpha(alpha)
            self.screen.blit(sup, (
                self.ANCHO // 2 - sup.get_width() // 2,
                self.ALTO // 2 - sup.get_height() // 2
            ))
            return

        self._dibujar_panel_ui()

        # ── Título ──
        titulo_sombra = self.fuente_titulo.render("HONOR KNIGHT", True, self.COLOR_SOMBRA_TXT)
        titulo = self.fuente_titulo.render("HONOR KNIGHT", True, self.COLOR_TEXTO)
        tx = self.ANCHO // 2 - titulo.get_width() // 2
        ty = 34
        self.screen.blit(titulo_sombra, (tx + 3, ty + 3))
        self.screen.blit(titulo, (tx, ty))

        # ── "Luna de Sangre" ──
        lsangre_sombra = self.fuente_opciones.render("LUNA DE SANGRE", True, self.COLOR_SOMBRA_TXT)
        lsangre = self.fuente_opciones.render("LUNA DE SANGRE", True, self.COLOR_ACENTO)
        lx = self.ANCHO // 2 - lsangre.get_width() // 2
        ly = ty + titulo.get_height() + 10
        self.screen.blit(lsangre_sombra, (lx + 2, ly + 2))
        self.screen.blit(lsangre, (lx, ly))

        sub = self.fuente_subtitulo.render(
            "BY  JACINTO  CORTEZ     .     2025",
            True, self.COLOR_TEXTO_OPACO
        )
        self.screen.blit(sub, (
            self.ANCHO // 2 - sub.get_width() // 2,
            ly + lsangre.get_height() + 12
        ))

        # ── "PRESS START" parpadeante, sobre el panel translúcido ──
        if self.blink_visible:
            ps = self.fuente_subtitulo.render("- PRESS START -", True, self.COLOR_ACENTO)
            self.screen.blit(ps, (
                self.ANCHO // 2 - ps.get_width() // 2,
                368
            ))

        # ── Opciones ──
        for i, opcion in enumerate(self.opciones):
            rect = self._opcion_rect(i)
            activo = (i == self.opcion_seleccionada)

            if activo:
                pygame.draw.rect(self.screen, (14, 8, 10), rect)
                pygame.draw.rect(self.screen, self.COLOR_ACENTO, rect, 1)
                pygame.draw.rect(self.screen, self.COLOR_ACENTO_OSC,
                                  (rect.x + 1, rect.y + 1, rect.width - 2, rect.height - 2), 1)
            else:
                pygame.draw.rect(self.screen, (30, 26, 30, 120), rect, 1)

            color_label = self.COLOR_TEXTO if activo else self.COLOR_TEXTO_OPACO

            if activo and self.blink_visible:
                cur = pygame.Surface((4, 4))
                cur.fill(self.COLOR_ACENTO)
                self.screen.blit(cur, (rect.x + 8, rect.y + rect.height // 2 - 2))
                self.screen.blit(cur, (rect.right - 14, rect.y + rect.height // 2 - 2))

            txt_sombra = self.fuente_opciones.render(opcion.upper(), True, self.COLOR_SOMBRA_TXT)
            texto = self.fuente_opciones.render(opcion.upper(), True, color_label)
            tx2 = self.ANCHO // 2 - texto.get_width() // 2
            ty2 = rect.y + rect.height // 2 - texto.get_height() // 2
            if activo:
                self.screen.blit(txt_sombra, (tx2 + 2, ty2 + 2))
            self.screen.blit(texto, (tx2, ty2))

        pygame.draw.rect(self.screen, (60, 50, 55),
                          (40, self.ALTO - 54, self.ANCHO - 80, 1))

        footer = self.fuente_footer.render(
            "UP/DOWN  MOVER     ENTER/CLIC  CONFIRMAR",
            True, self.COLOR_TEXTO_OPACO
        )
        self.screen.blit(footer, (
            self.ANCHO // 2 - footer.get_width() // 2,
            self.ALTO - 40
        ))