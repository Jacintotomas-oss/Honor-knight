import pygame
from mecanicas.npc import NPC
import json


#clase nueva para npc de mujer
class WomanNPC(NPC):
    def __init__(self, x, y, nombre, sprite_path="assets/sprites/NPC/women/plebe.png", wallet=None):
        super().__init__(x, y, nombre, sprite_path, wallet)

        #colisiones
        self.rect = pygame.Rect(self.x, self.y, 128, 128)

        #cargar dialogos de mujer
        with open("assets/dialogos/womenDialogos.json", "r", encoding="utf-8") as f:
                datos = json.load(f)
                self.dialogos = datos.get(self.nombre, {})

