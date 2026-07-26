import pygame
from mecanicas.Player import Player

class P1(Player):
    def __init__(self, x, y, speed=200):
        super().__init__(x, y)
        self.speed = speed

        # Sobreescribir sprite idle
        idle_raw = pygame.image.load("assets/sprites/p1/p1.png").convert_alpha()
        self.idle_sprite = pygame.transform.scale(idle_raw, (128, 128))
        self.image = self.idle_sprite

        # Cargar nuevo spritesheet
        self.sprite_sheet = pygame.image.load(
            "assets/sprites/p1/p1Spritesheet.png"
        ).convert_alpha()

        # Recalcular dimensiones del nuevo spritesheet
        sheet_width, sheet_height = self.sprite_sheet.get_size()
        self.frame_width = sheet_width // self.columns
        self.frame_height = sheet_height // self.rows

        # Regenerar animaciones con el nuevo spritesheet
        self.animations = {
            "down":  [self.get_frame(col, 0) for col in range(4)],
            "up":    [self.get_frame(col, 1) for col in range(4)],
            "left":  [self.get_frame(col, 2) for col in range(4)],
            "right": [self.get_frame(col, 3) for col in range(4)],
        }

        self.rect = pygame.Rect(self.x, self.y, 128, 128)