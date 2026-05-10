#clase de objetos para el inventario y para el mundo del juego
import pygame

class Objeto:
    def __init__(self):
        self.nombre = "objeto"
        self.descripcion = "descripcion del objeto"
        self.sprite = None
        self.cantidad = 1

    