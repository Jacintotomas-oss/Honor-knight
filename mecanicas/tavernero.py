import pygame
from mecanicas.npc import NPC


class Tavernero(NPC):
    def __init__(self):
        super().__init__(
            x=450,
            y=150,  # detrás de la barra
            nombre="tavernero",
            sprite_path="assets/sprites/NPC/Tavernero/tavernero.png"
        )