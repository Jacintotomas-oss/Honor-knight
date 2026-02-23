import pygame 

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 200

        # cargamos el sprit
        self.idle = pygame.image.load("assets/sprites/Tom/prota02.png").convert_alpha()
        self.walk1 = pygame.image.load("assets/sprites/Tom/walk 1.png").convert_alpha()
        self.walk2 = pygame.image.load("assets/sprites/Tom/walk 01.png").convert_alpha()

        # hacemos Escalado
        self.idle = pygame.transform.scale(self.idle, (128,128))
        self.walk1 = pygame.transform.scale(self.walk1, (128,128))
        self.walk2 = pygame.transform.scale(self.walk2, (128,128))

        self.walk_frames = [self.walk1, self.walk2]

        self.image = self.idle

        # ===== DIRECCIÓN =====
        self.direction = "down"   # preparado para futuro

        # estas varibles usaremos para la animacion
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15

    def handle_input(self, dt):
        pass

    def update(self, dt):
        keys = pygame.key.get_pressed()
        moving = False

        # ahi definimos con condiciones el movimiento del personaje dependiendo de las teclas que se presionen y ademas se actualiza la direccion del personaje para el sistema de animacion y volteo automatico
        if keys[pygame.K_w]:
            self.y -= self.speed * dt
            self.direction = "up"
            moving = True

        if keys[pygame.K_s]:
            self.y += self.speed * dt
            self.direction = "down"
            moving = True

        if keys[pygame.K_a]:
            self.x -= self.speed * dt
            self.direction = "left"
            moving = True

        if keys[pygame.K_d]:
            self.x += self.speed * dt
            self.direction = "right"
            moving = True

        # este es el sistema de la animacion se usa primero una condicional y luego utilizamos las variables definidas anteriormente para controlar el tiempo entre frames y el cambio de imagen dependiendo de si el personaje se esta moviendo o no 
        if moving:
            self.animation_timer += dt

            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)

            base_image = self.walk_frames[self.current_frame]
        else:
            self.current_frame = 0
            base_image = self.idle

        # hacemos un volteo de la imagen con pygame.transform.flip dependiendo de la direccion del personaje para que se vea mas natural el movimiento hacia la izquierda o derecha sin necesidad de tener sprites separados para cada direccion.
        if self.direction == "left":
            self.image = pygame.transform.flip(base_image, True, False)
        else:
            self.image = base_image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))