import pygame
from game import Game
from scenes.menu import MenuScene

pygame.init()

ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Honor Knight")

reloj = pygame.time.Clock()

game = Game(pantalla)
game.change_scene(MenuScene(game))

ejecutando = True
while ejecutando:
    dt = reloj.tick(60) / 1000

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        game.handle_event(evento)

    game.update(dt)
    game.draw()
    pygame.display.flip()

pygame.quit()
