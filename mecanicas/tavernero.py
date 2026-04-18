import pygame
from mecanicas.npc import NPC


class Tavernero(NPC):
    def __init__(self, wallet=None):  # ← agregar wallet=None
        super().__init__(
            x=450,
            y=150,
            nombre="tavernero",
            sprite_path="assets/sprites/NPC/Tavernero/tavernero.png",
            wallet=wallet  # ← pasar wallet al padre
        )