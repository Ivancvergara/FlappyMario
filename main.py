import pygame
from pathlib import Path
from pygame.locals import *
import random


pygame.init()

### Elemento Clock para controlar el movimiento
clock = pygame.time.Clock()
fps = 30

anchoPantalla = 500
altoPantalla = 650

pantalla = pygame.display.set_mode((anchoPantalla, altoPantalla))
pygame.display.set_caption("Flappy Mario")

#Cargando música y sonidos

musicaFondo = pygame.mixer.Sound("assets/principal.mp3")
sonidoSalto = pygame.mixer.Sound("assets/salto.wav")
sonidoMuerte = pygame.mixer.Sound("assets/muerto.wav")


#Definiendo fuente
fuenteGameOver = pygame.font.SysFont('Bauhaus 93', 25)
fuentePuntaje = pygame.font.SysFont('Bauhaus 93', 60)

#Definiendo color
blanco = (255, 255, 255)

#Definiendo variables del juego
velocidad = 8
gravedad = 1
desplazamientoPiso = 0
velocidadJuego = 6
gameOver = False
vuelo = False
espacioTubo = 150
frecuenciaTubo = 1500 #Milisegundos
ultimoTubo = pygame.time.get_ticks() - frecuenciaTubo
ancho_piso = 2 * anchoPantalla
altura_piso = 100
puntaje = 0
pasarTuberia = False

#Manejo de Archivo Mejor Puntaje
current_path = Path.cwd()
file_Path = current_path / "mejorPuntaje.txt"

#Cargando imágenes
fondo = pygame.image.load("assets/fondo.png")
fondo = pygame.transform.scale(fondo, (anchoPantalla, altoPantalla))
piso = pygame.image.load("assets/piso1.png")
img_GameOver = pygame.image.load("assets/gameover.png")


def textoFelicitacion(texto, fuenteGameOver, colorTexto, x, y):
    img = fuenteGameOver.render(texto, True, colorTexto)
    pantalla.blit(img, (x, y))

def textoMejorPuntaje(texto, fuenteGameOver, colorTexto, x, y):
    img = fuenteGameOver.render(texto, True, colorTexto)
    pantalla.blit(img, (x, y))

def textoPuntaje(texto, fuentePuntaje, colorTexto, x, y):
    img = fuentePuntaje.render(texto, True, colorTexto)
    pantalla.blit(img, (x, y))

def escrituraPuntaje():
    #Manejo de Archivo (Escritura, sobreescribiendo todo)
    with open(file_Path, "w") as file:
        file.write(str(puntaje))

class lecturaPuntaje:
    #Manejo de Archivo (Sólo Lectura)
    with open(file_Path) as file:
        content = file.read()

def reset_game():
    grupo_tubo.empty()
    mario.rect.x = 100
    mario.rect.y = int(altoPantalla / 2)
    puntaje = 0
    return puntaje

musicaFondo.set_volume(0.2)
musicaFondo.play()

#Clase para crear a Mario
class Mario(pygame.sprite.Sprite):

    #Función para crear un sprite de 3 Marios
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'assets/mario{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

        self.speed = velocidad

        
    #Función para controlar el movimiento de Mario
    def update(self):
        self.speed += gravedad


        # Actualizar altura
        if vuelo == True:
            self.rect[1] += self.speed

        if gameOver == False:

            #Manejo de la animación
            self.counter += 1
            cuentaColeo = 5

            if self.counter > cuentaColeo:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

    #Función para controlar la velocidad del cambio entre un sprite y otro
    def jump(self):
        self.speed = -velocidad
        

#Clase para crear el tubo
class Tubo(pygame.sprite.Sprite):

    def __init__(self, x, y, posicion):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/tubo.png")
        self.rect = self.image.get_rect()
        #Posición 1 es para el tubo superior, y el -1 para tubo inferior
        if posicion == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(espacioTubo / 2)]
        if posicion == -1:
            self.rect.topleft = [x, y + int(espacioTubo / 2)]
    
    #Movimiento de la tubería
    def update(self):
        self.rect.x -= velocidadJuego
        if self.rect.right < 0:
            self.kill()

class juegoTerminado():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #draw button
        pantalla.blit(self.image, (self.rect.x, self.rect.y))
        return action


grupo_mario = pygame.sprite.Group()
grupo_tubo = pygame.sprite.Group()

mario = Mario(100, int(altoPantalla / 2))

grupo_mario.add(mario)

posicionPiso = posicionPiso = altoPantalla - piso.get_height()

juegoTerminado = juegoTerminado((anchoPantalla/2) - 96, (altoPantalla/2) - 30, img_GameOver)

run = True
while run:
    clock.tick(fps)

    #Dibujar fondo
    pantalla.blit(fondo, (0,0))

    grupo_mario.draw(pantalla)
    grupo_mario.update()
    grupo_tubo.draw(pantalla)

    #Dibujar piso
    pantalla.blit(piso, (desplazamientoPiso, posicionPiso))

    #Puntaje
    if len(grupo_tubo) > 0:
        if grupo_mario.sprites()[0].rect.left > grupo_tubo.sprites()[0].rect.left\
            and grupo_mario.sprites()[0].rect.right < grupo_tubo.sprites()[0].rect.right\
            and pasarTuberia == False:
            pasarTuberia = True
        if pasarTuberia == True:
            if grupo_mario.sprites()[0].rect.left > grupo_tubo.sprites()[0].rect.right:
                puntaje += 1
                pasarTuberia = False

    textoPuntaje(str(puntaje), fuentePuntaje, blanco, int(anchoPantalla / 2), 20)
    
    #Busca de colisión
    if pygame.sprite.groupcollide(grupo_mario, grupo_tubo, False, False) or mario.rect.top < 0:
        gameOver = True
        
    #Chequeo si Mario tiene un tope en el suelo
    if mario.rect.bottom > posicionPiso:
        gameOver = True
        vuelo = False

    if gameOver == False and vuelo == True:

        #Generación de nuevas tuberías
        ahora = pygame.time.get_ticks()
        if ahora - ultimoTubo > frecuenciaTubo:
            alturaTubo = random.randint(-100, 100)
            tubo_inferior = Tubo(anchoPantalla, (altoPantalla/2) + alturaTubo, -1)
            tubo_superior = Tubo(anchoPantalla, (altoPantalla/2) + alturaTubo, 1)
            grupo_tubo.add(tubo_inferior)
            grupo_tubo.add(tubo_superior)
            ultimoTubo = ahora

        #Dibuja y desplaza el piso
        desplazamientoPiso -= velocidadJuego
        if abs(desplazamientoPiso) > 35:
            desplazamientoPiso = 0
        
        grupo_tubo.update()

    #Checar GameOver y reiniciar
    if gameOver == True:
        if puntaje > int(lecturaPuntaje.content):
            escrituraPuntaje()
            textoFelicitacion("¡Felicidades has superado el Mejor Puntaje!", fuenteGameOver, blanco, 5, int((altoPantalla / 5) * 3))
            textoMejorPuntaje("El Mejor Puntaje era de: " + lecturaPuntaje.content, fuenteGameOver, blanco, int((anchoPantalla / 2) - 120), int((altoPantalla / 5) * 3.5))
            textoPuntaje("Tu Puntaje fue de: " + str(puntaje), fuenteGameOver, blanco, int((anchoPantalla / 2) - 100), int((altoPantalla / 5) * 4))
        else:
            textoFelicitacion("No has superado el Mejor Puntaje :(", fuenteGameOver, blanco, int(anchoPantalla / 8), int((altoPantalla / 5) * 3))
            textoMejorPuntaje("El Mejor Puntaje es: " + lecturaPuntaje.content, fuenteGameOver, blanco, int((anchoPantalla / 2) - 100), int((altoPantalla / 5) * 3.5))
            textoPuntaje("Tu Puntaje fue de: " + str(puntaje), fuenteGameOver, blanco, int((anchoPantalla / 2) - 100), int((altoPantalla / 5) * 4))
        if juegoTerminado.draw() == True:
            gameOver = False
            puntaje = reset_game()
            

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == KEYDOWN and vuelo == False and gameOver == False:
            if event.key == K_SPACE:
                vuelo = True         
               
        mario.jump()
        sonidoSalto.play()
        sonidoSalto.set_volume(0.1)         

    pygame.display.update()

pygame.quit()