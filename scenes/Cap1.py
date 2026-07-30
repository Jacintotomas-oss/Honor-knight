import pygame
import random
from Personajes2.p1 import P1
from mecanicas.particulas import SistemaParticulas

class Cap1:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.P1 = P1(100, 100)

        self.background = pygame.image.load("assets/backgrounds/cap1.png").convert()
        self.background_tumba = pygame.image.load("assets/backgrounds/tumba.png").convert()
        self.fondo_actual = self.background

        self.P1.x = 200
        self.P1.y = 250

        self.obstaculos = [
            pygame.Rect(37, 77, 939, 61),
            pygame.Rect(25, 127, 20, 744),
            pygame.Rect(881, 111, 104, 380),
            pygame.Rect(49, 775, 392, 88),
            pygame.Rect(697, 751, 304, 112),
            pygame.Rect(713, 851, 280, 144),
            pygame.Rect(645, 831, 80, 148),
            pygame.Rect(57, 859, 400, 128),
        ]

        # ── Fade de entrada ──
        self.fade_alpha = 255
        self.fade_duracion = 2.0
        self.fade_timer = 0.0
        self.fade_activo = True

        # ── Partículas ambiente ──
        self.particulas = SistemaParticulas()
        self.particulas.agregar_emisor(200, 100, "hoja", 0.8)
        self.particulas.agregar_emisor(600, 80,  "hoja", 1.2)
        self.particulas.agregar_emisor(0,   80,  "neblina", 1.8)
        self.particulas.agregar_emisor(160, 60,  "neblina", 2.0)
        self.particulas.agregar_emisor(320, 50,  "neblina", 1.9)
        self.particulas.agregar_emisor(480, 70,  "neblina", 2.1)
        self.particulas.agregar_emisor(640, 55,  "neblina", 1.8)
        self.particulas.agregar_emisor(800, 80,  "neblina", 2.0)

        # ── Spritesheet cavar — 4 filas x 4 columnas ──
        self.sheet_cavar = pygame.image.load(
            "assets/sprites/p1/cavar.png").convert_alpha()
        sw, sh = self.sheet_cavar.get_size()
        self.cavar_cols = 4
        self.cavar_rows = 4
        self.cavar_fw = sw // self.cavar_cols
        self.cavar_fh = sh // self.cavar_rows

        print(f"Cavar sheet: {sw}x{sh} → frame: {self.cavar_fw}x{self.cavar_fh}")

        # Extraer frames — mismo sistema que Player.py
        self.frames_cavar = {
            "down":  [self._frame_cavar(col, 0) for col in range(4)],
            "right": [self._frame_cavar(col, 1) for col in range(4)],
            "left":  [self._frame_cavar(col, 2) for col in range(4)],
            "up":    [self._frame_cavar(col, 3) for col in range(4)],
        }

        # ── Estado de cavar ──
        self.zona_cavar = pygame.Rect(350, 350, 120, 100)
        self.cavando = False
        self.progreso_cavar = 0.0
        self.tumba_cavada = False
        self.frame_cavar_actual = 0
        self.timer_cavar = 0.0
        self.velocidad_anim_cavar = 0.15  # igual que Player.animation_speed

        # ── Partículas de tierra ──
        self.particulas_tierra = []

        # ── Fuente ──
        self.font = pygame.font.SysFont("Georgia", 14)
        self.font_barra = pygame.font.SysFont("Georgia", 13)

    def _frame_cavar(self, col, row):
        """Extrae frame usando el mismo método de Player para consistencia visual."""
        sheet_orig = self.P1.sprite_sheet
        fw_orig    = self.P1.frame_width
        fh_orig    = self.P1.frame_height

        self.P1.sprite_sheet = self.sheet_cavar
        self.P1.frame_width  = self.cavar_fw
        self.P1.frame_height = self.cavar_fh

        frame = self.P1.get_frame(col, row)

        self.P1.sprite_sheet = sheet_orig
        self.P1.frame_width  = fw_orig
        self.P1.frame_height = fh_orig

        return frame

    def _salpicar_tierra(self):
        cx = self.zona_cavar.centerx
        cy = self.zona_cavar.bottom - 20
        for _ in range(random.randint(4, 8)):
            angulo_izq = random.uniform(0.3, 1.2)
            angulo_der = random.uniform(0.3, 1.2)
            lado = random.choice([-1, 1])
            velocidad = random.uniform(2.5, 5.0)
            self.particulas_tierra.append({
                "x":        float(cx + random.randint(-15, 15)),
                "y":        float(cy),
                "vx":       lado * velocidad * angulo_izq,
                "vy":       -velocidad * angulo_der,
                "vida":     1.0,
                "duracion": random.uniform(0.3, 0.7),
                "tamano":   random.randint(3, 8),
                "color":    random.choice([
                    (101, 67, 33),
                    (80,  50, 20),
                    (120, 85, 40),
                    (90,  60, 25),
                    (110, 75, 35),
                ])
            })

    def handle_event(self, event):
        pass

    def iniciar_musica(self):
        pygame.mixer.music.load("assets/sounds/prologoMusic.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

    def update(self, dt):
        old_x = self.P1.x
        old_y = self.P1.y

        self.particulas.update(dt)

        # ── Actualizar partículas de tierra ──
        for p in self.particulas_tierra:
            p["vida"] -= dt / p["duracion"]
            p["x"]   += p["vx"]
            p["vy"]  += dt * 10  # gravedad
            p["y"]   += p["vy"]
            p["vx"]  *= 0.95     # fricción horizontal
        self.particulas_tierra = [
            p for p in self.particulas_tierra if p["vida"] > 0
        ]

        # ── Fade de entrada ──
        if self.fade_activo:
            self.fade_timer += dt
            progreso = self.fade_timer / self.fade_duracion
            self.fade_alpha = int((1 - progreso) * 255)
            if self.fade_timer >= self.fade_duracion:
                self.fade_alpha = 0
                self.fade_activo = False

        # ── Cavar ──
        teclas = pygame.key.get_pressed()
        cerca_tumba = self.P1.rect.colliderect(self.zona_cavar)
        tiene_pala = True

        if cerca_tumba and tiene_pala and not self.tumba_cavada and teclas[pygame.K_j]:
            self.P1.modo_cavar = True
            self.cavando = True
            self.progreso_cavar = min(1.0, self.progreso_cavar + dt * 0.08)

            self.timer_cavar += dt
            if self.timer_cavar >= self.velocidad_anim_cavar:
                self.timer_cavar = 0.0
                self.frame_cavar_actual = (self.frame_cavar_actual + 1) % 4
                self._salpicar_tierra()

            direccion = self.P1.direction if self.P1.direction in self.frames_cavar else "down"
            self.P1.image = self.frames_cavar[direccion][self.frame_cavar_actual]
            self.P1.rect.topleft = (int(self.P1.x), int(self.P1.y))

            if self.progreso_cavar >= 1.0:
                self.tumba_cavada = True
                self.fondo_actual = self.background_tumba
                self.cavando = False
                self.P1.modo_cavar = False

        else:
            self.P1.modo_cavar = False
            self.cavando = False
            self.P1.update(dt)

        # ── Colisiones ──
        for obstacul in self.obstaculos:
            if self.P1.rect.colliderect(obstacul):
                self.P1.x = old_x
                self.P1.y = old_y
                self.P1.rect.topleft = (int(old_x), int(old_y))

        # ── Cambio de escena ──
        if self.P1.y > 500:
            from scenes.CapB import CapB
            self.game.change_scene(self.game.get_scene("CapB", CapB))

    def draw(self):
        self.screen.blit(self.fondo_actual, (0, 0))
        self.particulas.draw(self.screen)

        # ── Partículas de tierra ──
        for p in self.particulas_tierra:
            alpha = int(max(0, p["vida"] * 255))
            tam = p["tamano"]
            sup = pygame.Surface((tam * 2, tam * 2), pygame.SRCALPHA)
            pygame.draw.circle(sup, (*p["color"], alpha), (tam, tam), tam)
            self.screen.blit(sup, (int(p["x"] - tam), int(p["y"] - tam)))

        self.P1.draw(self.screen)

        # ── Indicador J ──
        if self.P1.rect.colliderect(self.zona_cavar) and not self.tumba_cavada:
            hint = self.font.render("[J] Cavar", True, (220, 190, 120))
            borde = self.font.render("[J] Cavar", True, (0, 0, 0))
            hx = self.P1.rect.centerx - hint.get_width() // 2
            hy = self.P1.rect.top - 30
            self.screen.blit(borde, (hx + 1, hy + 1))
            self.screen.blit(hint,  (hx, hy))

        # ── Barra de progreso ──
        if self.cavando and not self.tumba_cavada:
            bx = 400 - 100
            by = 558
            bw = 200
            bh = 14

            # Sombra
            pygame.draw.rect(self.screen, (0, 0, 0),
                             (bx + 2, by + 2, bw, bh), border_radius=4)
            # Fondo
            pygame.draw.rect(self.screen, (25, 14, 6),
                             (bx, by, bw, bh), border_radius=4)
            # Relleno con gradiente simulado
            fill_w = int(bw * self.progreso_cavar)
            if fill_w > 0:
                pygame.draw.rect(self.screen, (160, 100, 40),
                                 (bx, by, fill_w, bh // 2), border_radius=4)
                pygame.draw.rect(self.screen, (139, 90, 43),
                                 (bx, by + bh // 2, fill_w, bh - bh // 2),
                                 border_radius=4)
            # Borde
            pygame.draw.rect(self.screen, (80, 50, 20),
                             (bx, by, bw, bh), 1, border_radius=4)

            # Label con sombra
            label = self.font_barra.render("Cavando...", True, (200, 160, 80))
            lsombra = self.font_barra.render("Cavando...", True, (0, 0, 0))
            lx = bx + bw // 2 - label.get_width() // 2
            self.screen.blit(lsombra, (lx + 1, by - 19))
            self.screen.blit(label,   (lx, by - 20))

        # ── Fade entrada ──
        if self.fade_activo:
            fade_surf = pygame.Surface((800, 600))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(self.fade_alpha)
            self.screen.blit(fade_surf, (0, 0))

        # DEBUG zona cavar — quitar cuando esté bien posicionada
        pygame.draw.rect(self.screen, (255, 255, 0), self.zona_cavar, 2)