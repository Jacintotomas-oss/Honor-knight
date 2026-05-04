import pygame
from mecanicas.status import Status  # ← ruta correcta

class Player:
    def __init__(self, x, y):
        self.x = x
        self.status = Status(max_health=100)
        self.y = y
        self.speed = 200

        

        # Carga del sprite sheet de movimiento
        self.sprite_sheet = pygame.image.load(
            "assets/sprites/Tom/spritesheets.Tom01.png"
        ).convert_alpha()

        sheet_width, sheet_height = self.sprite_sheet.get_size()
        print(f"Sprite sheet cargado: {sheet_width}x{sheet_height}")

        # Carga del sprite idle
        idle_raw = pygame.image.load(
            "assets/sprites/Tom/prota02.png"
        ).convert_alpha()
        self.idle_sprite = pygame.transform.scale(idle_raw, (128, 128))

        # El spritesheet es 4 columnas x 4 filas (408x612 → ~102x153 por frame)
        self.columns = 4
        self.rows = 4

        self.frame_width  = sheet_width  // self.columns   # 102
        self.frame_height = sheet_height // self.rows       # 153

        print(f"Frame size: {self.frame_width}x{self.frame_height}")

        # ─── Mapeo de filas según lo que se ve en el spritesheet ───
        # Fila 0 → down  (frente, con "T" en cabeza)
        # Fila 1 → up    (de espaldas / capa)
        # Fila 2 → left  (perfil izquierdo)
        # Fila 3 → right (perfil derecho)
        self.animations = {
            "down":  [self.get_frame(col, 0) for col in range(4)],
            "up":    [self.get_frame(col, 1) for col in range(4)],
            "left":  [self.get_frame(col, 2) for col in range(4)],
            "right": [self.get_frame(col, 3) for col in range(4)],
        }

        # Estado inicial
        self.direction       = "down"
        self.image           = self.animations["down"][0]
        self.current_frame   = 0
        self.animation_timer = 0
        self.animation_speed = 0.15   # segundos por frame

        self.rect = pygame.Rect(self.x, self.y, 128, 128)  # caja de colisiones pequeña

    # ──────────────────────────────────────────────
    def get_frame(self, col, row):
        """Extrae un frame del spritesheet y lo escala a 128x128."""
        frame = pygame.Surface(
            (self.frame_width, self.frame_height),
            pygame.SRCALPHA
        )
        frame.blit(
            self.sprite_sheet,
            (0, 0),
            (
                col * self.frame_width,
                row * self.frame_height,
                self.frame_width,
                self.frame_height,
            )
        )
        return pygame.transform.scale(frame, (128, 128))

    # ──────────────────────────────────────────────
    def update(self, dt):
        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_w]:
            self.y -= self.speed * dt
            self.direction = "up"
            moving = True
        elif keys[pygame.K_s]:
            self.y += self.speed * dt
            self.direction = "right"
            moving = True

        if keys[pygame.K_a]:
            self.x -= self.speed * dt
            self.direction = "left"
            moving = True
        elif keys[pygame.K_d]:
            self.x += self.speed * dt
            self.direction = "down"
            moving = True

        #sincronizando el react con la posicion
        self.rect.topleft = (int(self.x), int(self.y))
        if moving:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                frames = self.animations[self.direction]
                self.current_frame = (self.current_frame + 1) % len(frames)
            self.image = self.animations[self.direction][self.current_frame]
        else:
            self.animation_timer = 0
            self.current_frame   = 0
            self.image = self.idle_sprite

    # ──────────────────────────────────────────────
    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))