import pygame

class Inventario:
    def __init__(self, wallet):
        self.wallet = wallet
        self.visible = False
        self.font_titulo = pygame.font.SysFont("Arial", 28)
        self.font = pygame.font.SysFont("Arial", 18)
        self.font_small = pygame.font.SysFont("Arial", 15)
    
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
        panel_w, panel_h = 500, 420
        panel_x = ancho // 2 - panel_w // 2
        panel_y = alto // 2 - panel_h // 2
        pygame.draw.rect(screen, (30, 20, 10), (panel_x, panel_y, panel_w, panel_h), border_radius=10)
        pygame.draw.rect(screen, (139, 90, 43), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=10)

        # Título
        titulo = self.font_titulo.render("Inventario de Tom", True, (220, 190, 120))
        screen.blit(titulo, (panel_x + panel_w // 2 - titulo.get_width() // 2, panel_y + 16))

        # Línea separadora
        pygame.draw.line(screen, (139, 90, 43),
                         (panel_x + 20, panel_y + 55),
                         (panel_x + panel_w - 20, panel_y + 55), 1)

        y = panel_y + 70

        # ── Créditos ──
        cred_label = self.font.render("Créditos:", True, (180, 180, 180))
        cred_valor = self.font.render(f"{self.wallet.creditos} cr", True, (100, 220, 100))
        screen.blit(cred_label, (panel_x + 30, y))
        screen.blit(cred_valor, (panel_x + 160, y))
        y += 35

        # ── Deudas ──
        deuda_label = self.font.render("Deudas:", True, (180, 180, 180))
        screen.blit(deuda_label, (panel_x + 30, y))
        if self.wallet.deudas:
            deuda_total = self.font.render(f"-{self.wallet.total_deudas()} cr", True, (220, 80, 80))
            screen.blit(deuda_total, (panel_x + 160, y))
            y += 28
            for deuda in self.wallet.deudas:
                detalle = self.font_small.render(
                    f"  • {deuda['acreedor']}: {deuda['monto']} cr", True, (200, 120, 120))
                screen.blit(detalle, (panel_x + 30, y))
                y += 22
        else:
            sin_deuda = self.font.render("Ninguna", True, (100, 220, 100))
            screen.blit(sin_deuda, (panel_x + 160, y))
            y += 35

        y += 10
        pygame.draw.line(screen, (139, 90, 43),
                         (panel_x + 20, y),
                         (panel_x + panel_w - 20, y), 1)
        y += 14

        # ── Items ──
        items_label = self.font.render("Items:", True, (180, 180, 180))
        screen.blit(items_label, (panel_x + 30, y))
        y += 28
        if self.wallet.items:
            for item in self.wallet.items:
                item_texto = self.font_small.render(
                    f"  • {item['nombre']}  x{item['cantidad']}", True, (210, 190, 150))
                screen.blit(item_texto, (panel_x + 30, y))
                y += 22
        else:
            vacio = self.font_small.render("  Sin items por ahora.", True, (130, 130, 130))
            screen.blit(vacio, (panel_x + 30, y))

        # Instrucción cerrar
        cerrar = self.font_small.render("Presiona I para cerrar", True, (100, 100, 100))
        screen.blit(cerrar, (panel_x + panel_w // 2 - cerrar.get_width() // 2, panel_y + panel_h - 28))