
from mecanicas.wallet import Wallet

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.current_scene = None
        self.wallet = Wallet(creditos_iniciales=1000)
        self.escenas = {}

    def get_scene(self, nombre, clase):
        if nombre not in self.escenas:
            self.escenas[nombre] = clase(self)
        return self.escenas[nombre]
            
    #funcion paraa cambiar de escena
    def change_scene(self, new_scene):
        self.current_scene = new_scene
    #funcion hande_event esto va a manejar los eventos del juego
    def handle_event(self, event):
        if self.current_scene:
            self.current_scene.handle_event(event)
    #funcion update esto va a actualizar el estado del juego
    def update(self,dt):
        self.current_scene.update(dt)
    #funcion draw esto va a dibujar en la pantalla
    def draw(self):
        #dibujar pantalla completa al jugar
        self.current_scene.draw()
        