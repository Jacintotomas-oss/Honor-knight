import pygame

class NPC:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 100

        self.sprite_sheet = pygame.image.load(
            "assets/sprites/NPC/Bardo/bardo.png"
        ).convert_alpha()

        # Escalar al mismo tamaño que Tom (128x128)
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (128, 128))

       #Ajustar el rect también
        self.rect = pygame.Rect(self.x, self.y, 128, 128)
    def draw(self, screen):
        screen.blit(self.sprite_sheet, (self.x, self.y))