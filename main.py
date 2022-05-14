from winsound import PlaySound
import pygame
from pathlib import Path
from pygame.locals import *
import random


pygame.init()

### Elemento Clock para controlar el movimiento
clock = pygame.time.Clock()
fps = 30

ancho_pantalla = 500
alto_pantalla = 650

pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Flappy Mario")

#Cargando música y sonidos

pygame.mixer.music.load("assets/principal.wvb")
pygame.mixer.music.play()

sonido_salto = pygame.mixer.Sound("assets/salto.wav")
sonido_muerte = pygame.mixer.Sound("assets/muerto.wav")

#Definiendo fuente
fuente_GO = pygame.font.SysFont('Bauhaus 93', 25)
fuente_puntaje = pygame.font.SysFont('Bauhaus 93', 60)

#Definiendo color
blanco = (255, 255, 255)

#Definiendo variables del juego
velocidad = 8
gravedad = 1
desplazamiento_piso = 0
velocidad_juego = 6
game_over = False
vuelo = False
espacio_tubo = 150
frecuencia_tubo = 1500 #Milisegundos
ultimo_tubo = pygame.time.get_ticks() - frecuencia_tubo
ancho_piso = 2 * ancho_pantalla
altura_piso = 100
puntaje = 0
pasar_tuberia = False
PlaySound = True

#Manejo de Archivo Mejor Puntaje
current_path = Path.cwd()
file_Path = current_path / "mejorPuntaje.txt"

#Cargando imágenes
fondo = pygame.image.load("assets/fondo.png")
fondo = pygame.transform.scale(fondo, (ancho_pantalla, alto_pantalla))
piso = pygame.image.load("assets/piso1.png")
img_game_over = pygame.image.load("assets/gameOver.png")


def textoFelicitacion(texto, fuente_GO, colorTexto, x, y):
    img = fuente_GO.render(texto, True, colorTexto)
    pantalla.blit(img, (x, y))

def textoMejorPuntaje(texto, fuente_GO, colorTexto, x, y):
    img = fuente_GO.render(texto, True, colorTexto)
    pantalla.blit(img, (x, y))

def textoPuntaje(texto, fuente_puntaje, colorTexto, x, y):
    img = fuente_puntaje.render(texto, True, colorTexto)
    pantalla.blit(img, (x, y))

def escrituraPuntaje():
    #Manejo de Archivo (Escritura, sobreescribiendo todo)
    with open(file_Path, "w") as file:
        file.write(str(puntaje))

def lecturaPuntaje():
    #Manejo de Archivo (Sólo Lectura)
    with open(file_Path) as file:
        content = file.read()
        return content

def reset_game():
    grupo_tubo.empty()
    mario.rect.x = 100
    mario.rect.y = int(alto_pantalla / 2)
    puntaje = 0
    return puntaje

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

        if game_over == False:

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
    
    def sonido_salto(self):
        sonido_salto.play()
        sonido_salto.set_volume(0.6)
    
    def sonido_muerte(self):
        sonido_muerte.play(0)
        sonido_muerte.set_volume(0.2)       

#Clase para crear el tubo
class Tubo(pygame.sprite.Sprite):

    def __init__(self, x, y, posicion):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/tubo.png")
        self.rect = self.image.get_rect()
        #Posición 1 es para el tubo superior, y el -1 para tubo inferior
        if posicion == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(espacio_tubo / 2)]
        if posicion == -1:
            self.rect.topleft = [x, y + int(espacio_tubo / 2)]
    
    #Movimiento de la tubería
    def update(self):
        self.rect.x -= velocidad_juego
        if self.rect.right < 0:
            self.kill()

class juego_terminado():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        #draw button
        pantalla.blit(self.image, (self.rect.x, self.rect.y))
        return action

grupo_mario = pygame.sprite.Group()
grupo_tubo = pygame.sprite.Group()

mario = Mario(100, int(alto_pantalla / 2))

grupo_mario.add(mario)

posicion_piso = alto_pantalla - piso.get_height()

juego_terminado = juego_terminado((ancho_pantalla/2) - 96, (alto_pantalla/2) - 30, img_game_over)

run = True
while run:
    
    clock.tick(fps)

    #Dibujar fondo
    pantalla.blit(fondo, (0,0))

    grupo_mario.draw(pantalla)
    grupo_mario.update()
    grupo_tubo.draw(pantalla)

    #Dibujar piso
    pantalla.blit(piso, (desplazamiento_piso, posicion_piso))

    #Puntaje
    if len(grupo_tubo) > 0:
        if grupo_mario.sprites()[0].rect.left > grupo_tubo.sprites()[0].rect.left\
            and grupo_mario.sprites()[0].rect.right < grupo_tubo.sprites()[0].rect.right\
            and pasar_tuberia == False:
            pasar_tuberia = True
        if pasar_tuberia == True:
            if grupo_mario.sprites()[0].rect.left > grupo_tubo.sprites()[0].rect.right:
                puntaje += 1
                pasar_tuberia = False

    textoPuntaje(str(puntaje), fuente_puntaje, blanco, int(ancho_pantalla / 2), 20)
    
    #Busca de colisión con Tubos
    if pygame.sprite.groupcollide(grupo_mario, grupo_tubo, False, False) or mario.rect.top < 0:
        game_over = True
        vuelo = False

    #Chequeo si Mario tiene un tope en el suelo
    if mario.rect.bottom > posicion_piso:
        game_over = True
        vuelo = False

    if game_over == False and vuelo == True:

        #Generación de nuevas tuberías
        ahora = pygame.time.get_ticks()
        if ahora - ultimo_tubo > frecuencia_tubo:
            alturaTubo = random.randint(-100, 100)
            tubo_inferior = Tubo(ancho_pantalla, (alto_pantalla/2) + alturaTubo, -1)
            tubo_superior = Tubo(ancho_pantalla, (alto_pantalla/2) + alturaTubo, 1)
            grupo_tubo.add(tubo_inferior)
            grupo_tubo.add(tubo_superior)
            ultimo_tubo = ahora

        #Dibuja y desplaza el piso
        desplazamiento_piso -= velocidad_juego
        if abs(desplazamiento_piso) > 35:
            desplazamiento_piso = 0
        
        grupo_tubo.update()

    #Checar game_over y reiniciar
    if game_over == True:
        if(PlaySound):
            pygame.mixer.Sound.play(sonido_muerte)
            PlaySound = False
            pygame.mixer.music.stop()
        ultimo_puntaje = int(lecturaPuntaje())
        if puntaje >= ultimo_puntaje:
            textoFelicitacion("¡Felicidades has superado el Mejor Puntaje!", fuente_GO, blanco, 5, int((alto_pantalla / 5) * 3))
            textoMejorPuntaje("El Mejor Puntaje era de: " + str(ultimo_puntaje), fuente_GO, blanco, int((ancho_pantalla / 2) - 120), int((alto_pantalla / 5) * 3.5))
            textoPuntaje("Tu Puntaje fue de: " + str(puntaje), fuente_GO, blanco, int((ancho_pantalla / 2) - 100), int((alto_pantalla / 5) * 4))
        else:
            textoFelicitacion("No has superado el Mejor Puntaje :(", fuente_GO, blanco, int(ancho_pantalla / 8), int((alto_pantalla / 5) * 3))
            textoMejorPuntaje("El Mejor Puntaje es: " + str(ultimo_puntaje), fuente_GO, blanco, int((ancho_pantalla / 2) - 100), int((alto_pantalla / 5) * 3.5))
            textoPuntaje("Tu Puntaje fue de: " + str(puntaje), fuente_GO, blanco, int((ancho_pantalla / 2) - 100), int((alto_pantalla / 5) * 4))
        
        juego_terminado.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if puntaje >= ultimo_puntaje:
                escrituraPuntaje()
            run = False
        if event.type == KEYDOWN and vuelo == False and game_over == False:
            if event.key == K_SPACE:
                vuelo = True
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                if puntaje >= ultimo_puntaje:
                    escrituraPuntaje()
                reset_game()
                puntaje = reset_game()
                game_over = False
                PlaySound = True
                sonido_muerte.stop()
                pygame.mixer.music.play()
        mario.jump()
        if vuelo == True:
            mario.sonido_salto()                
    pygame.display.update()
pygame.quit()