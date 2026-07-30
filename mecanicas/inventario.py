import pygame
from mecanicas.objetos import Objeto

class Inventario:
    def __init__(self, wallet):
        self.wallet = wallet
        self.visible = False
        self.font_titulo = pygame.font.SysFont("Arial", 28)
        self.font = pygame.font.SysFont("Arial", 18)
        self.font_small = pygame.font.SysFont("Arial", 15)
        self.item_seleccionado = None
        self.item_rects = []  # rects de cada item para detectar clic
        self.menu_activo = False  # muestra el menu contextual 
        self.menu_pos = (0,0) #posicion
        self.accion_pendiente = None
        self.menu_rects = []
       

    def toggle(self):
        self.visible = not self.visible
        if not self.visible:
            self.item_seleccionado = None

    def handle_event(self, event):
        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Si el menú contextual está activo
            if self.menu_activo and hasattr(self, 'menu_rects'):
                opciones = ["Tomar", "Dejar", "Ver"]
                for i, rect in enumerate(self.menu_rects):
                    if rect.collidepoint(event.pos):
                        self.accion_pendiente = (opciones[i], self.item_seleccionado)
                        self.menu_activo = False
                        return
                # Si clic fuera del menú lo cierra
                self.menu_activo = False
                return

            # Clic en un item
            for i, rect in enumerate(self.item_rects):
                if rect.collidepoint(event.pos):
                    if i < len(self.wallet.items):
                        self.item_seleccionado = self.wallet.items[i]
                        self.menu_activo = True
                        self.menu_pos = event.pos

    def draw(self, screen):
        if not self.visible:
            return

        ancho, alto = screen.get_size()
        mouse_pos = pygame.mouse.get_pos()

        overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        panel_w, panel_h = 500, 420
        panel_x = ancho // 2 - panel_w // 2
        panel_y = alto // 2 - panel_h // 2
        pygame.draw.rect(screen, (30, 20, 10),
                         (panel_x, panel_y, panel_w, panel_h), border_radius=10)
        pygame.draw.rect(screen, (139, 90, 43),
                         (panel_x, panel_y, panel_w, panel_h), 2, border_radius=10)

        titulo = self.font_titulo.render("Inventario", True, (220, 190, 120))
        screen.blit(titulo, (panel_x + panel_w // 2 - titulo.get_width() // 2, panel_y + 16))

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
            deuda_total = self.font.render(
                f"-{self.wallet.total_deudas()} cr", True, (220, 80, 80))
            screen.blit(deuda_total, (panel_x + 160, y))
            y += 28
            for deuda in self.wallet.deudas:
                detalle = self.font_small.render(
                    f"  • {deuda['acreedor']}: {deuda['monto']} cr",
                    True, (200, 120, 120))
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

        self.item_rects = []

        if self.wallet.items:
            for item in self.wallet.items:
                item_rect = pygame.Rect(panel_x + 25, y - 2, panel_w - 50, 24)
                self.item_rects.append(item_rect)

                # Hover
                hover = item_rect.collidepoint(mouse_pos)
                # Seleccionado
                seleccionado = (self.item_seleccionado == item)

                if seleccionado:
                    pygame.draw.rect(screen, (80, 50, 20), item_rect, border_radius=4)
                    pygame.draw.rect(screen, (139, 90, 43), item_rect, 1, border_radius=4)
                elif hover:
                    pygame.draw.rect(screen, (50, 35, 15), item_rect, border_radius=4)

                cantidad = getattr(item, 'cantidad', 1)
                color = (255, 220, 100) if seleccionado else (210, 190, 150)
                item_texto = self.font_small.render(
                    f"  • {item.nombre}  x{cantidad}", True, color)
                screen.blit(item_texto, (panel_x + 30, y))
                y += 26
        else:
            vacio = self.font_small.render("  Sin items por ahora.", True, (130, 130, 130))
            screen.blit(vacio, (panel_x + 30, y))

        # ── Panel de detalle del item seleccionado ──
        if self.item_seleccionado:
            det_y = panel_y + panel_h - 80
            pygame.draw.line(screen, (139, 90, 43),
                             (panel_x + 20, det_y),
                             (panel_x + panel_w - 20, det_y), 1)
            nombre = self.font.render(
                self.item_seleccionado.nombre, True, (220, 190, 120))
            screen.blit(nombre, (panel_x + 30, det_y + 10))

        cerrar = self.font_small.render(
            "Presiona I para cerrar", True, (100, 100, 100))
        screen.blit(cerrar, (
            panel_x + panel_w // 2 - cerrar.get_width() // 2,
            panel_y + panel_h - 28))
        if self.menu_activo and self.item_seleccionado:
            opciones = ["Tomar", "Dejar", "Ver"]
            mx, my = self.menu_pos
            ancho_menu = 120
            alto_opcion = 28
            alto_menu = alto_opcion * len(opciones)

            # Fondo del menú
            pygame.draw.rect(screen, (25, 18, 10),
                             (mx, my, ancho_menu, alto_menu), border_radius=6)
            pygame.draw.rect(screen, (139, 90, 43),
                             (mx, my, ancho_menu, alto_menu), 1, border_radius=6)

            mouse_pos = pygame.mouse.get_pos()
            self.menu_rects = []

            for i, opcion in enumerate(opciones):
                rect_op = pygame.Rect(mx, my + i * alto_opcion, ancho_menu, alto_opcion)
                self.menu_rects.append(rect_op)

                # Hover
                if rect_op.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (60, 38, 15), rect_op, border_radius=4)

                texto_op = self.font_small.render(opcion, True, (220, 190, 120))
                screen.blit(texto_op, (
                    mx + 12,
                    my + i * alto_opcion + alto_opcion // 2 - texto_op.get_height() // 2
                ))