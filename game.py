import json
import os
from mecanicas.wallet import Wallet
from mecanicas.objetos import Objeto

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.current_scene = None
        self.wallet = Wallet(creditos_iniciales=1000)
        self.escenas = {}

        if os.path.exists("assets/JSON/save.json"):
            with open("assets/JSON/save.json", "r") as f:
                self.save = json.load(f)


        else:
            # crear valores por defecto
            self.save = {
                "creditos": 1000,
                "objetosRecogidos": [],
                "escenaActual": "tavern",
                "jugador_x": 100,
                "jugador_y": 100
            }
        
        
    def save_game(self):
        with open("assets/JSON/save.json", "w") as f:
            json.dump(self.save, f, identity = 4)

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
        