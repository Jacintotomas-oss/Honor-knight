import pygame 

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.speed = 200
        
        self.image = pygame.image.load("assets/sprites/Tom/prota01.png"). convert_alpha()
        self.image = pygame.transform.scale(self.image, (128, 128))
    def handle_input(self,dt):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.y += self.speed * dt
        if keys[pygame.K_a]:
            self.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.x += self.speed * dt
    def update(self,dt):
        self.handle_input(dt)
        
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))

    