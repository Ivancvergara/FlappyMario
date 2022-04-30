from turtle import Screen
import pygame, sys
from pygame.locals import *

anchoPantalla = 400
altoPantalla = 650
velocidad = 10
gravedad = 1
velocidad_Juego = 10

ancho_piso = 2 * anchoPantalla
altura_piso = 100

#Clase para crear a Mario
class Mario(pygame.sprite.Sprite):

    #Función para crear un sprite de 3 Marios
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load("assets/mario1.png").convert_alpha(),
                        pygame.image.load("assets/mario2.png").convert_alpha(),
                        pygame.image.load("assets/mario3.png").convert_alpha()]

        self.speed = velocidad

        self.current_image = 0

        self.image = pygame.image.load("assets/mario1.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = anchoPantalla / 2
        self.rect[1] = altoPantalla / 2

    #Función para controlar el movimiento de Mario (VER VIDEO PARA CORROBORAR)
    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]

        self.speed += gravedad

        # Actualizar altura
        self.rect[1] += self.speed

    #Función para controlar la velocidad del cambio entre un sprite y otro
    def bump(self):
        self.speed = -velocidad



#Clase para crear el piso
class Piso(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("assets/piso.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (ancho_piso, altura_piso))
        
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = altoPantalla - altura_piso
    
    def update(self):
        self.rect[0] -= velocidad_Juego

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

pygame.init()
pantalla = pygame.display.set_mode((anchoPantalla, altoPantalla))


fondo = pygame.image.load("assets/fondo.png")
fondo = pygame.transform.scale(fondo, (anchoPantalla, altoPantalla))


grupo_mario = pygame.sprite.Group()
mario = Mario()
grupo_mario.add(mario)


grupo_piso = pygame.sprite.Group()
for i in range(2):
    piso = Piso(ancho_piso * i)
    grupo_piso.add(piso)

### Elemento Clock para controlar el movimiento de Mario.
clock = pygame.time.Clock()

while True:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                mario.bump()

    pantalla.blit(fondo, (0,0))

    # Ciclo IF para crear piso "infinito"
    if is_off_screen(grupo_piso.sprites()[0]):
        grupo_piso.remove(grupo_piso.sprites()[0])
        
        nuevo_piso = Piso(ancho_piso - 10)
        grupo_piso.add(nuevo_piso)


    grupo_mario.update()
    grupo_piso.update()

    grupo_mario.draw(pantalla)
    grupo_piso.draw(pantalla)

    if pygame.sprite.groupcollide(grupo_mario, grupo_piso, False, False, pygame.sprite.collide_mask):
        #Game Over
        input()
        break
    
    pygame.display.update()