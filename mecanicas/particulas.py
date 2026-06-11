import pygame
import random
import math

class Particulas:  #clase padre para particulas
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.vida = 1.0
        self.tiempo = 0.0
        self.duracion = random.uniform(0.5, 10.5)  # duración aleatoria entre 0.5 y 10.5 segundos
        self.tamano = random.randint(2, 5)  # tamaño aleatorio entre 2 y 5 
        self.color = (0, 0, 0)  # color por defecto será negro, pero se asignará según el tipo de partícula
        self.oscilacion = 0.0  # para el movimiento oscilante de las hojas
        self.vx = random.uniform(-1.5, 1.5)  # velocidad horizontal aleatoria sera entre 0.3 y 1.5
        self.vy = random.uniform(0.5, 0.5)  # velocidad vertical aleatoria (caída)
        self.ancho = self.tamano * 2  # valor por defecto


        if self.tipo == "hoja":
            self.color = (20, 100, 20)  # verde para hojas

        elif self.tipo == "chispas":
            self.color = (255, 215, 0)  # dorado para chispas

        elif self.tipo == "neblina":
            self.vx = random.uniform(-0.2, 0.2)   # movimiento horizontal lento
            self.vy = random.uniform(-0.02, 0.02)  # casi sin movimiento vertical
            self.radio = random.randint(130, 220)
            self.duracion = random.uniform(10.0, 18.0)  # vive más tiempo
            self.color =  random.choice([
                (140, 150, 170),  # gris azulado medio
                (120, 130, 155),  # un poco más oscuro
                (100, 110, 135),  # el más oscuro de los tres
   # casi negro azulado                    
            ])           
             # Precalcular las 6 capas una sola vez
            self.capas_sup = []
            for i in range(6, 0, -1):
                factor = i / 6
                rx = int(self.radio * factor)
                ry = int(rx * 0.45)
                sup = pygame.Surface((rx * 2, ry * 2), pygame.SRCALPHA)
                pygame.draw.ellipse(sup, (*self.color, 45), (0, 0, rx * 2, ry * 2))
                self.capas_sup.append((sup, rx, ry))
                        

        
    def update (self, dt): #en update se actualiza la posición y la vida de la partícula
        self.tiempo += dt
        self.vida = 1.0 - (self.tiempo / self.duracion)  # va de 1.0 a 0.0

        if self.tipo == "hoja":
            self.oscilacion += dt * 2  # el ángulo del seno avanza con el tiempo
            self.x += self.vx + math.sin(self.oscilacion) * 0.5
            # sin() devuelve un valor entre -1 y 1 que oscila suavemente
            # multiplicado por 0.5 da un vaivén suave de lado a lado
            self.y += self.vy  # siempre cae hacia abajo

        elif self.tipo == "neblina":
            self.x += self.vx
            self.y += self.vy

    def EstaViva(self): #método para saber si la partícula sigue viva
        return self.vida > 0

    def draw(self, screen):
        if self.tipo == "neblina":
            alpha_global = int(self.vida * 180)
            for sup_base, rx, ry in self.capas_sup:
                sup = sup_base.copy()
                sup.set_alpha(alpha_global)
                screen.blit(sup, (int(self.x - rx), int(self.y - ry)))

        else:
            # hojas, chispas, etc.
            alpha = int(max(0, min(255, self.vida * 255)))
            sup = pygame.Surface((self.ancho, self.tamano * 2), pygame.SRCALPHA)
            pygame.draw.rect(sup, (*self.color, alpha), (0, 0, self.ancho, self.tamano * 2))
            screen.blit(sup, (int(self.x - self.tamano), int(self.y - self.tamano)))
#clase sistema Particulas

class SistemaParticulas:
    def __init__(self):
        self.particulas = []
        self.emisores = []  # lista de emisores activos
    

    def agregar_emisor(self, x, y, tipo, intervalo):
        self.emisores.append({
        "x": x,
        "y": y,
        "tipo": tipo,
        "intervalo": intervalo,
        "timer": 0.0
    })

    def update(self, dt):
        for emisor in self.emisores:
            emisor["timer"] += dt
            if emisor["timer"] >= emisor["intervalo"]:
                emisor["timer"] = 0
                import random
                offset_x = random.randint(-60, 60)
                self.particulas.append(Particulas(emisor["x"] + offset_x, emisor["y"], emisor["tipo"]))
        for particula in self.particulas:
            particula.update(dt)
        # Eliminar partículas muertas
        self.particulas = [p for p in self.particulas if p.EstaViva()]

    def draw(self, screen):
        for particula in self.particulas:
            particula.draw(screen)
        