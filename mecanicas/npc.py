import pygame
import json

class NPC:
    def __init__(self, x, y, nombre, sprite_path="assets/sprites/NPC/Bardo/bardo.png", wallet=None):
        self.x = x
        self.y = y
        self.nombre = nombre
        self.speed = 100
        self.wallet = wallet  # referencia al wallet del jugador

        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (128, 128))
        self.rect = pygame.Rect(self.x, self.y, 128, 128)

        with open("assets/dialogos/dialogosNpc.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.dialogos = datos.get(self.nombre, {})

        # Estado del diálogo
        self.hablando = False
        self.nodo_actual = "inicio"
        self.esperando_opcion = False
        self.respuesta_activa = None
        self.mensaje_error = None  # "Sin fondos suficientes"

        # Estado propina
        self.modo_propina = False
        self.propina_valor = 5  # valor inicial

        self.font = pygame.font.SysFont("Arial", 16)
        self.font_opciones = pygame.font.SysFont("Arial", 14)

    def verificar_distancia(self, player_rect):
        distancia = abs(self.rect.centerx - player_rect.centerx) + \
                    abs(self.rect.centery - player_rect.centery)
        if distancia >= 150:
            self._resetear()

    def _resetear(self):
        self.hablando = False
        self.nodo_actual = "inicio"
        self.esperando_opcion = False
        self.respuesta_activa = None
        self.mensaje_error = None
        self.modo_propina = False
        self.propina_valor = 5

    def activar(self):
        if not self.hablando:
            self.hablando = True
            self.esperando_opcion = True
            self.respuesta_activa = None

    def elegir_opcion(self, indice):
        if not self.esperando_opcion:
            return
        nodo = self.dialogos.get(self.nodo_actual, {})
        opciones = nodo.get("opciones", [])
        if indice >= len(opciones):
            return

        opcion = opciones[indice]
        costo = opcion.get("costo", 0)

        # Verificar si tiene fondos
        if costo > 0 and self.wallet:
            if not self.wallet.gastar(costo):
                self.mensaje_error = f"No tienes suficientes créditos. ({costo} cr)"
                return

        self.mensaje_error = None
        self.respuesta_activa = opcion["respuesta_npc"]
        self.esperando_opcion = False

    def cerrar_respuesta(self):
        if not self.respuesta_activa:
            return
        nodo = self.dialogos.get(self.nodo_actual, {})
        opciones = nodo.get("opciones", [])
        siguiente = "fin"
        for op in opciones:
            if op["respuesta_npc"] == self.respuesta_activa:
                siguiente = op.get("siguiente", "fin")
                break

        self.respuesta_activa = None

        if siguiente == "propina":
            self.modo_propina = True
            self.propina_valor = 5
            self.esperando_opcion = False
        elif siguiente == "fin" or siguiente not in self.dialogos:
            self._resetear()
        else:
            self.nodo_actual = siguiente
            self.esperando_opcion = True

    def ajustar_propina(self, direccion):
        """Sube o baja la propina con flechas ↑↓."""
        if direccion == "arriba":
            self.propina_valor = min(15, self.propina_valor + 1)
        else:
            self.propina_valor = max(5, self.propina_valor - 1)

    def confirmar_propina(self):
        """Presionar E confirma la propina."""
        if self.wallet:
            if self.wallet.gastar(self.propina_valor):
                self.modo_propina = False
                self.respuesta_activa = f"¡Muchas gracias por los {self.propina_valor} créditos, noble caballero!"
                self.esperando_opcion = False
            else:
                self.mensaje_error = "No tienes suficientes créditos."
        else:
            self.modo_propina = False
            self._resetear()

    def saltar_propina(self):
        """Presionar R salta la propina."""
        self.modo_propina = False
        self._resetear()

    def draw(self, screen):
        screen.blit(self.sprite_sheet, (self.x, self.y))
        if self.hablando or self.modo_propina:
            self._dibujar_burbuja(screen)

    def _dibujar_burbuja(self, screen):
        padding = 10
        max_ancho = 280
        alto_texto = self.font.get_height()
        alto_opciones = self.font_opciones.get_height()

        # Modo propina
        if self.modo_propina:
            lineas = ["¿Desea dejar una propina?"]
            ancho_burbuja = max_ancho
            alto_burbuja = padding * 2 + alto_texto * 2 + 60

            bx = self.x + 64 - ancho_burbuja // 2
            by = self.y - alto_burbuja - 15

            pygame.draw.rect(screen, (255, 255, 255), (bx, by, ancho_burbuja, alto_burbuja), border_radius=8)
            pygame.draw.rect(screen, (80, 50, 20), (bx, by, ancho_burbuja, alto_burbuja), 2, border_radius=8)

            texto = self.font.render("¿Desea dejar una propina?", True, (0, 0, 0))
            screen.blit(texto, (bx + padding, by + padding))

            valor = self.font_opciones.render(f"↑  {self.propina_valor} cr  ↓", True, (139, 90, 43))
            screen.blit(valor, (bx + ancho_burbuja // 2 - valor.get_width() // 2, by + padding + alto_texto + 10))

            confirmar = self.font_opciones.render("E — Dar propina   R — No dar", True, (100, 100, 100))
            screen.blit(confirmar, (bx + padding, by + alto_burbuja - alto_opciones - padding))

            if self.mensaje_error:
                error = self.font_opciones.render(self.mensaje_error, True, (200, 50, 50))
                screen.blit(error, (bx + padding, by + alto_burbuja - alto_opciones * 2 - padding))
            return

        # Modo normal
        nodo = self.dialogos.get(self.nodo_actual, {})
        texto_principal = self.respuesta_activa if self.respuesta_activa else nodo.get("texto", "...")
        opciones = [] if self.respuesta_activa else nodo.get("opciones", [])

        lineas = self._wrap_texto(texto_principal, max_ancho - padding * 2)
        ancho_burbuja = max_ancho
        alto_burbuja = padding * 2 + alto_texto * len(lineas)

        if opciones:
            alto_burbuja += 8
            for op in opciones:
                lineas_op = self._wrap_texto(f"x. {op['texto_tom']}", max_ancho - padding * 2)
                alto_burbuja += alto_opciones * len(lineas_op)

        bx = self.x + 64 - ancho_burbuja // 2
        by = self.y - alto_burbuja - 15

        pygame.draw.rect(screen, (255, 255, 255), (bx, by, ancho_burbuja, alto_burbuja), border_radius=8)
        pygame.draw.rect(screen, (80, 50, 20), (bx, by, ancho_burbuja, alto_burbuja), 2, border_radius=8)

        for i, linea in enumerate(lineas):
            sup = self.font.render(linea, True, (0, 0, 0))
            screen.blit(sup, (bx + padding, by + padding + i * alto_texto))

        # Mensaje error sin fondos
        if self.mensaje_error:
            error = self.font_opciones.render(self.mensaje_error, True, (200, 50, 50))
            screen.blit(error, (bx + padding, by + alto_burbuja + 5))

        if opciones:
            separador_y = by + padding + alto_texto * len(lineas) + 6
            pygame.draw.line(screen, (80, 50, 20),
                             (bx + padding, separador_y),
                             (bx + ancho_burbuja - padding, separador_y), 1)
            offset_y = separador_y + 6
            for i, op in enumerate(opciones):
                texto_op = f"{i + 1}. {op['texto_tom']}"
                lineas_op = self._wrap_texto(texto_op, max_ancho - padding * 2)
                for linea_op in lineas_op:
                    sup_op = self.font_opciones.render(linea_op, True, (139, 90, 43))
                    screen.blit(sup_op, (bx + padding, offset_y))
                    offset_y += alto_opciones

        cx = self.x + 64
        puntos = [(cx - 8, by + alto_burbuja), (cx + 8, by + alto_burbuja), (cx, by + alto_burbuja + 10)]
        pygame.draw.polygon(screen, (255, 255, 255), puntos)
        pygame.draw.lines(screen, (80, 50, 20), False, [puntos[0], puntos[2], puntos[1]], 2)

    def _wrap_texto(self, texto, ancho_max):
        palabras = texto.split(" ")
        lineas = []
        linea_actual = ""
        for palabra in palabras:
            prueba = linea_actual + palabra + " "
            if self.font.size(prueba)[0] > ancho_max:
                lineas.append(linea_actual.strip())
                linea_actual = palabra + " "
            else:
                linea_actual = prueba
        lineas.append(linea_actual.strip())
        return lineas