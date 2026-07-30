import pygame
from Personajes2.p1 import P1
from mecanicas.Dead import Dead
from mecanicas.inventario import Inventario
from mecanicas.status import Status
from mecanicas.particulas import SistemaParticulas
from mecanicas.objetos import Objeto

class CapB:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.P1 = P1(400, 200)
        self.wallet = game.wallet
        self.inventario = Inventario(self.wallet)
        self.status = Status(max_health=100)
        self.dialogo_e_disponible = None  # "bebe" o "mujer"
        self.background = pygame.image.load("assets/backgrounds/Cap1.2.png").convert_alpha()

        self.menu_activo = False  # muestra el menu contextual
        self.item_seleccionado = None  # item seleccionado en el inventario

        if self.menu_activo and self.item_seleccionado:
            opciones = ["Tomar", "Dejar", "Ver"]
            # dibujas los 3 botones en menu_pos

        # ── Colisiones ──
        self.obstaculos = [
            pygame.Rect(59, 797, 934, 125),
            pygame.Rect(12, 43, 111, 741),
            pygame.Rect(915, 63, 96, 725),
        ]

        # ── Fogata — centro del mapa ──
        # Coordenadas calibradas sobre el fondo real (1024x886 px):
        # el centro de las cenizas está en ~(510, 508)
        self.fogata_rect = pygame.Rect(452, 464, 116, 90)
        self.tiempo_en_fogata = 0.0
        self.en_llamas = False

        # ── Muerte ──
        self.muriendo = False
        self.muerte_timer = 0.0
        self.muerte_duracion = 3.0
        self.fade_muerte = 0
        self.font_muerte = pygame.font.SysFont("Georgia", 32)

        # ── Cadáveres ──
        self.cadaver_bebe = Dead(270, 390)
        self.sprite_bebe = pygame.transform.scale(
            pygame.image.load("assets/sprites/Deads/prologo/Baby.png").convert_alpha(),
            (48, 48)
        )

        self.cadaver_mujer = Dead(380, 370)
        self.sprite_mujer = pygame.transform.scale(
            pygame.image.load("assets/sprites/Deads/prologo/dead1prolo.png").convert_alpha(),
            (128, 128)
        )

        # ── Diálogos ──
        self.dialogo_activo = None
        self.dialogo_timer = 0.0
        self.dialogo_duracion = 4.0
        self.font_dialogo = pygame.font.SysFont("Georgia", 16)
        self.dialogo_bebe_mostrado = False
        self.dialogo_mujer_mostrado = False

        # ── Objetos del inventario ──
        espada = Objeto()
        espada.nombre = "Espada Bastarda"
        espada.sprite = None
        espada.rect = None

        pala = Objeto()
        pala.nombre = "Pala"
        pala.sprite = None
        pala.rect = None

        self.wallet.items.append(espada)
        self.wallet.items.append(pala)

        # ── Partículas fogata ──
        # Mismos offsets relativos que tenías, reubicados sobre el nuevo centro
        self.particulas = SistemaParticulas()
        self.particulas.agregar_emisor(510, 483, "humo", 0.3)
        self.particulas.agregar_emisor(505, 493, "ceniza", 0.8)
        self.particulas.agregar_emisor(507, 498, "fuego", 0.08)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.inventario.toggle()
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                self.status.toggle()
            if event.key == pygame.K_e:
                if self.dialogo_e_disponible == "bebe" and not self.dialogo_bebe_mostrado:
                    self.dialogo_activo = "Pronto estaremos juntos, pequeño..."
                    self.dialogo_timer = 0.0
                    self.dialogo_bebe_mostrado = True
                elif self.dialogo_e_disponible == "mujer" and not self.dialogo_mujer_mostrado:
                    self.dialogo_activo = "Debí estar con ustedes. Lo siento."
                    self.dialogo_timer = 0.0
                    self.dialogo_mujer_mostrado = True

        # pasar eventos al inventario para selección con mouse
        self.inventario.handle_event(event)

    def update(self, dt):
        # ── Si está muriendo, solo avanza el fade ──
        if self.muriendo:
            self.muerte_timer += dt
            self.fade_muerte = min(255, int((self.muerte_timer / self.muerte_duracion) * 255))
            if self.muerte_timer >= self.muerte_duracion:
                # Resetear save y volver al menú
                self.game.save["creditos"] = 1000
                self.game.save["objetosRecogidos"] = []
                self.game.save["escenaActual"] = "menu"
                self.game.wallet.creditos = 1000
                self.game.wallet.items = []
                self.game.save_game()
                from scenes.menu import MenuScene
                if "menu" in self.game.escenas:
                    del self.game.escenas["menu"]
                self.game.change_scene(MenuScene(self.game))
            return

        if self.inventario.visible or self.status.visible:
            return
        accion = self.inventario.accion_pendiente
        if accion:
            tipo, item = accion
            if tipo == "Tomar" and item.nombre == "Pala":
                self.P1.modo = "pala"
                #sprite con pala
                sprite_pala_raw = pygame.image.load("assets/sprites/p1/pala.png").convert_alpha()
                self.P1.idle_sprite = pygame.transform.scale(sprite_pala_raw, (128, 128))
                self.P1.image = self.P1.idle_sprite

                #spritesheet caminado con la pala
                self.P1.sprite_sheet = pygame.image.load(
                    "assets/sprites/p1/pala1c.png"
                ).convert_alpha()

                # Recalcular dimensiones del nuevo spritesheet
                sheet_width, sheet_height = self.P1.sprite_sheet.get_size()
                self.P1.frame_width = sheet_width // self.P1.columns
                self.P1.frame_height = sheet_height // self.P1.rows
                # Regenerar animaciones con el nuevo spritesheet
                self.P1.animations = {
                "down":  [self.P1.get_frame(col, 0) for col in range(4)],
                "up":    [self.P1.get_frame(col, 1) for col in range(4)],
                "left":  [self.P1.get_frame(col, 2) for col in range(4)],
                "right": [self.P1.get_frame(col, 3) for col in range(4)],
}

                self.P1.rect = pygame.Rect(self.P1.x, self.P1.y, 128, 128)
            elif tipo == "Dejar":
                self.wallet.items.remove(item)
            self.inventario.accion_pendiente = None

        old_x = self.P1.x
        old_y = self.P1.y

        self.P1.update(dt)
        self.status.update(dt)
        self.particulas.update(dt)
        

        # ── Colisiones ──
        for obstacul in self.obstaculos:
            if self.P1.rect.colliderect(obstacul):
                self.P1.x = old_x
                self.P1.y = old_y
                self.P1.rect.topleft = (int(old_x), int(old_y))

        # ── Cadáveres ──
        self.cadaver_bebe.update(dt)
        self.cadaver_bebe.verificar_proximidad(self.P1.rect, self.status)
        self.cadaver_mujer.update(dt)
        self.cadaver_mujer.verificar_proximidad(self.P1.rect, self.status)

        # ── Detectar proximidad para diálogo con E ──
        dist_bebe = abs(self.P1.rect.centerx - self.cadaver_bebe.rect.centerx) + \
                    abs(self.P1.rect.centery - self.cadaver_bebe.rect.centery)
        dist_mujer = abs(self.P1.rect.centerx - self.cadaver_mujer.rect.centerx) + \
                    abs(self.P1.rect.centery - self.cadaver_mujer.rect.centery)

        if dist_bebe < 100 and not self.dialogo_bebe_mostrado:
            self.dialogo_e_disponible = "bebe"
        elif dist_mujer < 120 and not self.dialogo_mujer_mostrado:
            self.dialogo_e_disponible = "mujer"
        else:
            self.dialogo_e_disponible = None

        if self.dialogo_activo:
            self.dialogo_timer += dt
            if self.dialogo_timer >= self.dialogo_duracion:
                self.dialogo_activo = None
        # ── Fogata ──
        if self.P1.rect.colliderect(self.fogata_rect):
            self.tiempo_en_fogata += dt
            self.status.health -= 2 * dt
            if self.tiempo_en_fogata >= 10.0:
                self.en_llamas = True
        else:
            self.tiempo_en_fogata = 0.0
            self.en_llamas = False

        if self.en_llamas:
            self.status.health -= 10 * dt
            self.particulas.agregar_emisor(
                self.P1.rect.centerx, self.P1.rect.top, "fuego", 0.05
            )

        # ── Verificar muerte ──
        self.status.health = max(0, self.status.health)
        self.status.higiene = max(0, self.status.higiene)

        if self.status.health <= 0 and not self.muriendo:
            self.muriendo = True
            self.muerte_timer = 0.0
            self.fade_muerte = 0

         #regresar a la escena anterior
        if self.P1.y < -50:
            from scenes.Cap1 import Cap1
            self.game.change_scene(self.game.get_scene("Cap1", Cap1))

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.sprite_bebe, self.cadaver_bebe.rect)
        self.screen.blit(self.sprite_mujer, self.cadaver_mujer.rect)

        self.particulas.draw(self.screen)
        self.P1.draw(self.screen)

        self.inventario.draw(self.screen)
        self.status.draw(self.screen)

        if self.dialogo_activo:
            self._dibujar_dialogo(self.dialogo_activo)
            

        # ── Pantalla de muerte ──
        if self.muriendo:
            fade = pygame.Surface((800, 600))
            fade.fill((0, 0, 0))
            fade.set_alpha(self.fade_muerte)
            self.screen.blit(fade, (0, 0))

            if self.muerte_timer > 1.5:
                texto = self.font_muerte.render("Has muerto.", True, (180, 50, 50))
                texto.set_alpha(min(255, int((self.muerte_timer - 1.5) / 1.5 * 255)))
                self.screen.blit(texto, (
                    400 - texto.get_width() // 2,
                    300 - texto.get_height() // 2
                ))
        # ── Indicador de interacción ──
        if self.dialogo_e_disponible:
            hint = self.font_dialogo.render("[E] Interactuar", True, (220, 190, 120))
            self.screen.blit(hint, (
                self.P1.rect.centerx - hint.get_width() // 2,
                self.P1.rect.top - 25
            ))

        # DEBUG
        #for obstaculo in self.obstaculos:
         #   pygame.draw.rect(self.screen, (255, 0, 0), obstaculo, 2)
        #pygame.draw.rect(self.screen, (0, 255, 0), self.P1.rect, 2)
        #pygame.draw.rect(self.screen, (255, 165, 0), self.fogata_rect, 2)


    def _dibujar_dialogo(self, texto):
        padding = 10
        lineas = self._wrap(texto, 300)
        alto = self.font_dialogo.get_height()
        alto_total = padding * 2 + alto * len(lineas)
        ancho = 320

        bx = self.P1.rect.centerx - ancho // 2
        by = self.P1.rect.top - alto_total - 15
        bx = max(5, min(bx, 795 - ancho))
        by = max(5, by)

        pygame.draw.rect(self.screen, (20, 15, 10),
                         (bx, by, ancho, alto_total), border_radius=6)
        pygame.draw.rect(self.screen, (139, 90, 43),
                         (bx, by, ancho, alto_total), 2, border_radius=6)

        for i, linea in enumerate(lineas):
            sup = self.font_dialogo.render(linea, True, (220, 190, 120))
            self.screen.blit(sup, (bx + padding, by + padding + i * alto))

    def _wrap(self, texto, ancho_max):
        palabras = texto.split(" ")
        lineas = []
        linea = ""
        for palabra in palabras:
            prueba = linea + palabra + " "
            if self.font_dialogo.size(prueba)[0] > ancho_max:
                lineas.append(linea.strip())
                linea = palabra + " "
            else:
                linea = prueba
        lineas.append(linea.strip())
        return lineas