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


        if self.tipo == "hoja":
            self.color = (34, 139, 34)  # verde para hojas

        elif self.tipo == "chispas":
            self.color = (255, 215, 0)  # dorado para chispas
        

        
    def update (self, dt): #en update se actualiza la posición y la vida de la partícula
        self.tiempo += dt
        self.vida = 1.0 - (self.tiempo / self.duracion)  # va de 1.0 a 0.0

        if self.tipo == "hoja":
            self.oscilacion += dt * 2  # el ángulo del seno avanza con el tiempo
            self.x += self.vx + math.sin(self.oscilacion) * 0.5
            # sin() devuelve un valor entre -1 y 1 que oscila suavemente
            # multiplicado por 0.5 da un vaivén suave de lado a lado
            self.y += self.vy  # siempre cae hacia abajo

    def EstaViva(self): #método para saber si la partícula sigue viva
        return self.vida > 0

    def draw(self, screen): #se dibuja la partícula con un círculo que se desvanece según su vida
        alpha = int(max(0, min(255, self.vida * 200)))
        # self.vida va de 1.0 a 0.0
        # multiplicado por 200 da un alpha entre 200 y 0
        # max(0, ...) evita valores negativos
        # min(255, ...) evita pasar de 255

        sup = pygame.Surface((self.tamano * 2, self.tamano * 2), pygame.SRCALPHA)
        # SRCALPHA permite transparencia en la superficie

        pygame.draw.circle(sup, (*self.color, alpha), (self.tamano, self.tamano), self.tamano)
        # *self.color desempaqueta (R, G, B) y le agrega el alpha → (R, G, B, alpha)

        screen.blit(sup, (int(self.x - self.tamano), int(self.y - self.tamano)))
        # resta self.tamano para centrar el círculo en x,y


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
                self.particulas.append(Particulas(emisor["x"], emisor["y"], emisor["tipo"]))

        for particula in self.particulas:
            particula.update(dt)
        # Eliminar partículas muertas
        self.particulas = [p for p in self.particulas if p.EstaViva()]

    def draw(self, screen):
        for particula in self.particulas:
            particula.draw(screen)
        