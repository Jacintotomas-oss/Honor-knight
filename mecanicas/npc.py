import pygame
import json

class NPC:
    def __init__(self, x, y, nombre, sprite_path="assets/sprites/NPC/Bardo/bardo.png"):
        self.x = x
        self.y = y
        self.nombre = nombre
        self.speed = 100

        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (128, 128))
        self.rect = pygame.Rect(self.x, self.y, 128, 128)

    
        # Cargar diálogos desde JSON
        with open("assets/dialogos/dialogosNpc.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.dialogos = datos.get(self.nombre, {})

        # Estado del diálogo
        self.hablando = False
        self.nodo_actual = "inicio"
        self.esperando_opcion = False
        self.respuesta_activa = None
        self.font = pygame.font.SysFont("Arial", 16)
        self.font_opciones = pygame.font.SysFont("Arial", 14)

    def verificar_distancia(self, player_rect):
        distancia = abs(self.rect.centerx - player_rect.centerx) + \
                    abs(self.rect.centery - player_rect.centery)
        if distancia >= 150:
            self._resetear()

    def _resetear(self):
        """Reinicia el estado del diálogo."""
        self.hablando = False
        self.nodo_actual = "inicio"
        self.esperando_opcion = False
        self.respuesta_activa = None

    def activar(self):
        """Presionar E activa el diálogo."""
        if not self.hablando:
            self.hablando = True
            self.esperando_opcion = True
            self.respuesta_activa = None

    def elegir_opcion(self, indice):
        """Tom elige una opción con las teclas 1, 2, 3."""
        if not self.esperando_opcion:
            return
        nodo = self.dialogos.get(self.nodo_actual, {})
        opciones = nodo.get("opciones", [])
        if indice < len(opciones):
            opcion = opciones[indice]
            self.respuesta_activa = opcion["respuesta_npc"]
            self.esperando_opcion = False

    def cerrar_respuesta(self):
        """Presionar E avanza al siguiente nodo o cierra."""
        if not self.respuesta_activa:
            return

        # Buscar el siguiente nodo según la opción elegida
        nodo = self.dialogos.get(self.nodo_actual, {})
        opciones = nodo.get("opciones", [])
        siguiente = "fin"
        for op in opciones:
            if op["respuesta_npc"] == self.respuesta_activa:
                siguiente = op.get("siguiente", "fin")
                break

        self.respuesta_activa = None

        if siguiente == "fin" or siguiente not in self.dialogos:
            self._resetear()
        else:
            self.nodo_actual = siguiente
            self.esperando_opcion = True

    def draw(self, screen):
        screen.blit(self.sprite_sheet, (self.x, self.y))
        if self.hablando:
            self._dibujar_burbuja(screen)

    def _dibujar_burbuja(self, screen):
        nodo = self.dialogos.get(self.nodo_actual, {})

        texto_principal = self.respuesta_activa if self.respuesta_activa else nodo.get("texto", "...")
        opciones = [] if self.respuesta_activa else nodo.get("opciones", [])

        padding = 10
        max_ancho = 280

        lineas = self._wrap_texto(texto_principal, max_ancho - padding * 2)

        alto_texto = self.font.get_height()
        alto_opciones = self.font_opciones.get_height()

        ancho_burbuja = max_ancho
        alto_burbuja = padding * 2 + alto_texto * len(lineas)

        # Calcular alto correcto para opciones con wrap
        if opciones:
            alto_burbuja += 8
            for op in opciones:
                lineas_op = self._wrap_texto(f"x. {op['texto_tom']}", max_ancho - padding * 2)
                alto_burbuja += alto_opciones * len(lineas_op)

        # Posición sobre el NPC
        bx = self.x + (128 // 2) - (ancho_burbuja // 2)
        by = self.y - alto_burbuja - 15

        # Fondo blanco y borde
        pygame.draw.rect(screen, (255, 255, 255), (bx, by, ancho_burbuja, alto_burbuja), border_radius=8)
        pygame.draw.rect(screen, (80, 50, 20), (bx, by, ancho_burbuja, alto_burbuja), 2, border_radius=8)

        # Texto principal
        for i, linea in enumerate(lineas):
            sup = self.font.render(linea, True, (0, 0, 0))
            screen.blit(sup, (bx + padding, by + padding + i * alto_texto))

        # Opciones de Tom
        if opciones:
            separador_y = by + padding + alto_texto * len(lineas) + 6
            pygame.draw.line(screen, (80, 50, 20), (bx + padding, separador_y), (bx + ancho_burbuja - padding, separador_y), 1)
            offset_y = separador_y + 6
            for i, op in enumerate(opciones):
                texto_op = f"{i + 1}. {op['texto_tom']}"
                lineas_op = self._wrap_texto(texto_op, max_ancho - padding * 2)
                for linea_op in lineas_op:
                    sup_op = self.font_opciones.render(linea_op, True, (139, 90, 43))
                    screen.blit(sup_op, (bx + padding, offset_y))
                    offset_y += alto_opciones

        # Triángulo apuntando al NPC
        cx = self.x + 64
        puntos = [(cx - 8, by + alto_burbuja), (cx + 8, by + alto_burbuja), (cx, by + alto_burbuja + 10)]
        pygame.draw.polygon(screen, (255, 255, 255), puntos)
        pygame.draw.lines(screen, (80, 50, 20), False, [puntos[0], puntos[2], puntos[1]], 2)

    def _wrap_texto(self, texto, ancho_max):
        """Divide un texto largo en líneas."""
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