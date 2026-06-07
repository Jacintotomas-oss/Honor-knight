import pygame
from mecanicas.npc import NPC
from Personajes2.p1 import P1



class Cap1:
    def __init__(self,game):
        self.game = game
        self.screen = game.screen
        self.P1 = P1(100, 100)
        

        

        self.background = pygame.image.load("assets/backgrounds/cap1.png").convert()
        self.P1.x = 200
        self.P1.y = 250

        self.obstaculos = [
            
            pygame.Rect(37, 77, 939, 61),  # 0
            pygame.Rect(25, 127, 20, 744),  # 1
            pygame.Rect(881, 111, 104, 380),  # 2
            pygame.Rect(49, 775, 392, 88),  # 3
            pygame.Rect(697, 751, 304, 112),  # 4
            pygame.Rect(713, 851, 280, 144),  # 5
            pygame.Rect(645, 831, 80, 148),  # 6
            pygame.Rect(57, 859, 400, 128),  # 7
        ]

        self.fade_alpha = 255
        self.fade_duracion = 2.0
        self.fade_timer = 0.0
        self.fade_activo = True

    def handle_event(self,event):
        pass
    def update (self,dt):

        old_x = self.P1.x
        old_y = self.P1.y

        self.P1.update(dt)

        for obstacul in self.obstaculos:
            if self.P1.rect.colliderect(obstacul):
                self.P1.x = old_x
                self.P1.y = old_y
                self.P1.rect.topleft = (self.P1.x, self.P1.y)

        if self.fade_activo:
            self.fade_timer += dt
            progreso = self.fade_timer / self.fade_duracion
            self.fade_alpha = int((1 - progreso) * 255)
            if self.fade_timer >= self.fade_duracion:
                self.fade_alpha = 0
                self.fade_activo = False
        
    def draw (self):
        self.screen.blit(self.background, (0, 0))
        self.P1.draw(self.screen)

        if self.fade_activo:
            fade_surf = pygame.Surface((800, 600))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(self.fade_alpha)
            self.screen.blit(fade_surf, (0, 0))

