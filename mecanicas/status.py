import pygame

class Status:
    def __init__(self, max_health=100):
        self.max_health = max_health
        self.health = max_health
        self.alive = True

        # Stats de supervivencia
        self.higiene = 100.0      # 0-100
        self.hambre = 100.0       # 0-100
        self.sed = 100.0          # 0-100
        self.herida = False
        self.infectado = False
        self.enfermedad = None    # None o nombre de la enfermedad

        # Tiempo real acumulado en segundos
        self.tiempo_total = 0.0

        # UI
        self.visible = False
        self.font_titulo = pygame.font.SysFont("Arial", 28)
        self.font = pygame.font.SysFont("Arial", 18)
        self.font_small = pygame.font.SysFont("Arial", 15)

    # ── Lógica de salud ──

    def recibir_dano(self, cantidad):
        if not self.alive:
            return
        self.health -= cantidad
        self.herida = True
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def curar(self, dt, tiene_medicina):
        if not self.alive:
            return
        if tiene_medicina:
            tasa = self.max_health / 86400    # cura completo en 1 dia
        else:
            tasa = self.max_health / 172800   # cura completo en 2 dias
        self.health += tasa * dt
        if self.health > self.max_health:
            self.health = self.max_health
            self.herida = False
            self.infectado = False

    def clasificar_herida(self):
        perdida = self.max_health - self.health
        if perdida <= self.max_health * 0.25:
            return "Leve"
        elif perdida <= self.max_health * 0.60:
            return "Moderada"
        else:
            return "Grave"

    # ── Degradación con el tiempo ──

    def update(self, dt):
        if not self.alive:
            return

        self.tiempo_total += dt

        # Higiene baja cada 110 horas reales (396000 segundos)
        self.higiene -= (100 / 396000) * dt
        self.higiene = max(0, self.higiene)

        # Sed baja cada 24 horas reales (86400 segundos)
        self.sed -= (100 / 86400) * dt
        self.sed = max(0, self.sed)

        # Hambre baja cada 72 horas reales (259200 segundos)
        self.hambre -= (100 / 259200) * dt
        self.hambre = max(0, self.hambre)

        # Infección si hay herida sin curar por más de 48h
        if self.herida and self.tiempo_total > 172800:
            self.infectado = True

        # Daño gradual por stats críticos
        if self.sed <= 0:
            self.recibir_dano(dt * 0.5)
        if self.hambre <= 0:
            self.recibir_dano(dt * 0.2)
        if self.infectado:
            self.recibir_dano(dt * 0.1)

    # ── UI ──

    def toggle(self):
        self.visible = not self.visible

    def draw(self, screen):
        if not self.visible:
            return

        ancho, alto = screen.get_size()

        # Fondo oscuro semitransparente
        overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Panel central
        panel_w, panel_h = 500, 460
        panel_x = ancho // 2 - panel_w // 2
        panel_y = alto // 2 - panel_h // 2
        pygame.draw.rect(screen, (30, 20, 10), (panel_x, panel_y, panel_w, panel_h), border_radius=10)
        pygame.draw.rect(screen, (139, 90, 43), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=10)

        # Título
        titulo = self.font_titulo.render("Estado de Tom", True, (220, 190, 120))
        screen.blit(titulo, (panel_x + panel_w // 2 - titulo.get_width() // 2, panel_y + 16))

        pygame.draw.line(screen, (139, 90, 43),
                         (panel_x + 20, panel_y + 55),
                         (panel_x + panel_w - 20, panel_y + 55), 1)

        y = panel_y + 70

        # Salud
        self._dibujar_barra(screen, panel_x + 30, y, "Salud",
                            self.health, self.max_health, (220, 80, 80))
        if self.herida:
            tipo = self.clasificar_herida()
            color = (200, 50, 50) if tipo == "Grave" else (200, 150, 50) if tipo == "Moderada" else (200, 200, 50)
            herida_txt = self.font_small.render(f"  Herida {tipo}" + (" — INFECTADA" if self.infectado else ""), True, color)
            screen.blit(herida_txt, (panel_x + 30, y + 28))
        y += 55

        # Higiene
        self._dibujar_barra(screen, panel_x + 30, y, "Higiene",
                            self.higiene, 100, (100, 180, 220))
        y += 55

        # Hambre
        self._dibujar_barra(screen, panel_x + 30, y, "Hambre",
                            self.hambre, 100, (200, 160, 80))
        y += 55

        # Sed
        self._dibujar_barra(screen, panel_x + 30, y, "Sed",
                            self.sed, 100, (80, 160, 220))
        y += 55

        # Enfermedad
        pygame.draw.line(screen, (139, 90, 43),
                         (panel_x + 20, y),
                         (panel_x + panel_w - 20, y), 1)
        y += 14

        enf_label = self.font.render("Enfermedad:", True, (180, 180, 180))
        screen.blit(enf_label, (panel_x + 30, y))
        if self.enfermedad:
            enf_valor = self.font.render(self.enfermedad, True, (220, 80, 80))
        else:
            enf_valor = self.font.render("Ninguna", True, (100, 220, 100))
        screen.blit(enf_valor, (panel_x + 180, y))

        # Instrucción cerrar
        cerrar = self.font_small.render("Presiona Shift para cerrar", True, (100, 100, 100))
        screen.blit(cerrar, (panel_x + panel_w // 2 - cerrar.get_width() // 2, panel_y + panel_h - 28))

    def _dibujar_barra(self, screen, x, y, label, valor, maximo, color):
        label_surf = self.font.render(f"{label}:", True, (180, 180, 180))
        screen.blit(label_surf, (x, y))

        barra_x = x + 120
        barra_w = 280
        barra_h = 16
        porcentaje = max(0, valor / maximo)

        # Fondo de la barra
        pygame.draw.rect(screen, (60, 40, 20), (barra_x, y + 2, barra_w, barra_h), border_radius=4)
        # Relleno
        if porcentaje > 0:
            pygame.draw.rect(screen, color, (barra_x, y + 2, int(barra_w * porcentaje), barra_h), border_radius=4)
        # Borde
        pygame.draw.rect(screen, (139, 90, 43), (barra_x, y + 2, barra_w, barra_h), 1, border_radius=4)

        # Porcentaje en texto
        pct_txt = self.font_small.render(f"{int(valor)}%", True, (200, 200, 200))
        screen.blit(pct_txt, (barra_x + barra_w + 8, y + 2))

        