import pygame
import random
import math

class Particulas:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.vida = 1.0
        self.tiempo = 0.0
        self.duracion = random.uniform(0.5, 10.5)
        self.tamano = random.randint(2, 5)
        self.color = (0, 0, 0)
        self.oscilacion = 0.0
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(0.5, 0.5)
        self.ancho = self.tamano * 2

        if self.tipo == "hoja":
            self.color = (20, 100, 20)

        elif self.tipo == "chispas":
            self.color = (255, 215, 0)

        elif self.tipo == "humo":
            self.vx = random.uniform(-0.3, 0.3)
            self.vy = random.uniform(-1.0, -0.5)
            self.tamano = random.randint(8, 20)
            self.ancho = self.tamano * 2
            self.duracion = random.uniform(2.0, 4.0)
            self.color = random.choice([
                (80, 80, 80),
                (100, 100, 100),
                (120, 120, 120)
            ])

        elif self.tipo == "ceniza":
            self.vx = random.uniform(-1.0, 1.0)
            self.vy = random.uniform(-0.5, -0.2)
            self.tamano = random.randint(2, 4)
            self.ancho = self.tamano * 2
            self.duracion = random.uniform(3.0, 6.0)
            self.color = (200, 200, 200)

        elif self.tipo == "fuego":
            self.vx = random.uniform(-0.5, 0.5)
            self.vy = random.uniform(-2.0, -1.0)
            self.tamano = random.randint(4, 10)
            self.ancho = self.tamano * 2
            self.duracion = random.uniform(0.3, 0.7)
            self.color = random.choice([
                (255, 200, 50),
                (255, 140, 0),
                (255, 80, 0)
            ])
        

        elif self.tipo == "neblina":
            self.vx = random.uniform(-0.2, 0.2)
            self.vy = random.uniform(-0.02, 0.02)
            self.radio = random.randint(130, 220)
            self.duracion = random.uniform(10.0, 18.0)
            self.color = random.choice([
                (140, 150, 170),
                (120, 130, 155),
                (100, 110, 135),
            ])
            self.capas_sup = []
            for i in range(6, 0, -1):
                factor = i / 6
                rx = int(self.radio * factor)
                ry = int(rx * 0.45)
                sup = pygame.Surface((rx * 2, ry * 2), pygame.SRCALPHA)
                pygame.draw.ellipse(sup, (*self.color, 45), (0, 0, rx * 2, ry * 2))
                self.capas_sup.append((sup, rx, ry))

    def update(self, dt):
        self.tiempo += dt
        self.vida = 1.0 - (self.tiempo / self.duracion)

        if self.tipo == "hoja":
            self.oscilacion += dt * 2
            self.x += self.vx + math.sin(self.oscilacion) * 0.5
            self.y += self.vy

        elif self.tipo == "neblina":
            self.x += self.vx
            self.y += self.vy

        elif self.tipo == "humo":
            self.x += self.vx
            self.y += self.vy
            self.tamano += dt * 3
            self.ancho = int(self.tamano * 2)

        elif self.tipo == "ceniza":
            self.oscilacion += dt
            self.x += self.vx + math.sin(self.oscilacion) * 0.3
            self.y += self.vy

        elif self.tipo == "fuego":
            self.x += self.vx
            self.y += self.vy
        elif self.tipo == "tierra":
            self.oscilacion += dt
            self.x += self.vx
            self.y += self.vy + math.sin(self.oscilacion) * 0.3
            self.vy += dt * 3  # gravedad

    def EstaViva(self):
        return self.vida > 0

    def draw(self, screen):
        if self.tipo == "neblina":
            alpha_global = int(self.vida * 180)
            for sup_base, rx, ry in self.capas_sup:
                sup = sup_base.copy()
                sup.set_alpha(alpha_global)
                screen.blit(sup, (int(self.x - rx), int(self.y - ry)))
        else:
            alpha = int(max(0, min(255, self.vida * 255)))
            sup = pygame.Surface((self.ancho, self.tamano * 2), pygame.SRCALPHA)
            pygame.draw.rect(sup, (*self.color, alpha), (0, 0, self.ancho, self.tamano * 2))
            screen.blit(sup, (int(self.x - self.tamano), int(self.y - self.tamano)))


class SistemaParticulas:
    def __init__(self):
        self.particulas = []
        self.emisores = []

    def agregar_emisor(self, x, y, tipo, intervalo):
        self.emisores.append({
            "x": x, "y": y,
            "tipo": tipo,
            "intervalo": intervalo,
            "timer": 0.0
        })

    def update(self, dt):
        for emisor in self.emisores:
            emisor["timer"] += dt
            if emisor["timer"] >= emisor["intervalo"]:
                emisor["timer"] = 0
                offset_x = random.randint(-60, 60)
                self.particulas.append(
                    Particulas(emisor["x"] + offset_x, emisor["y"], emisor["tipo"])
                )
        for particula in self.particulas:
            particula.update(dt)
        self.particulas = [p for p in self.particulas if p.EstaViva()]

    def draw(self, screen):
        for particula in self.particulas:
            particula.draw(screen)