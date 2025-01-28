import pygame
import random
import math
from pygame import mixer

pygame.init() # inicializar pygame 

# crear la pantalla
pantalla = pygame.display.set_mode((800,600))

# Titulo e icono 
pygame.display.set_caption("Invación espacial") # 32 px
icono = pygame.image.load("images/alien.png") # para cargarle imagenes
pygame.display.set_icon(icono)
fondo = pygame.image.load("images/galaxia_fondo.jpg")

# agregar musica
mixer.music.load('music/musicafondo.wav')
mixer.music.set_volume(0.3)
mixer.music.play(-1)
# jugador - datos
# protagonista 64px
# Para ubicarlos al medio 
"""
    Para ubircar al protagonista al medio
    Pantalla = 800x600
    Protagonista = 64px
    En el eje x = 800/2 = 400
    La img del protagonista mide 64 px la mitad es 32 px para que quede al medio 400-32 = 368 px
    Para ubicar en la parte inferior del eje X -> 600-64 = 536 
    Eje y - (Tamaño_imagen) 
"""
# Variable de jugador
img_jugador = pygame.image.load("images/astronave.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0


# Variable de enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos): 
    img_enemigo.append(pygame.image.load("images/enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# Variable de la bala 
img_bala = pygame.image.load("images/bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

# puntaje 
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf',32)
texto_x = 10
texto_y = 10

# texto final del juego
fuente_final = pygame.font.Font('font/CrazyStormDemoRegular.ttf',55)

def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER", True,(255,255,255))
    pantalla.blit(mi_fuente_final,(250,200))


# función mostrar puntaje 
def mostrar_puntaje(x,y):
    texto = fuente.render(f"Puntaje: {puntaje}",True, (255,255,255))
    pantalla.blit(texto, (x,y))

#Funcion jugador 
def jugador(x,y):
    pantalla.blit(img_jugador, (x, y)) # arrojar (imagen, (posicionX,posicionY))

#Funcion jugador 
def enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene], (x, y)) # arrojar (imagen, (posicionX,posicionY))

# función dispara bala
def disparar_bala(x,y):
    global bala_visible
    bala_visible=True
    pantalla.blit(img_bala, (x+16,y+10))

# función detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2-x_1,2)+math.pow(y_2-y_1,2)) #distancia entre dos puntos
    if distancia < 27:
        return True
    else:
        return False
    
# Función para mostrar el menú inicial
def mostrar_menu():
    fuente_menu = pygame.font.Font('freesansbold.ttf', 64)
    texto_menu = fuente_menu.render("Invación Espacial", True, (255, 255, 255))
    texto_iniciar = fuente.render("Presiona ESPACIO para comenzar", True, (255, 255, 255))
    texto_salir = fuente.render("Presiona ESC para salir", True, (255, 255, 255))
    
    pantalla.blit(texto_menu, (150, 200))
    pantalla.blit(texto_iniciar, (150, 350))
    pantalla.blit(texto_salir, (150, 400))

# Loop del menú inicial
en_menu = True
while en_menu:
    pantalla.blit(fondo, (0, 0))
    mostrar_menu()
    pygame.display.update()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            en_menu = False
            se_ejecuta = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                en_menu = False
            if evento.key == pygame.K_ESCAPE:
                en_menu = False
                se_ejecuta = False
#Loop del juego 
se_ejecuta = True
while se_ejecuta == True :
    pantalla.blit(fondo,(0,0))
    # iterar eventos
    for evento in pygame.event.get():
        # evento cerrar programa
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        # evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('music/disparo.mp3')
                sonido_bala.set_volume(0.35)
                sonido_bala.play()
                if bala_visible == False:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)
                
        # evento soltar flechas    
        if evento.type == pygame.KEYUP: # Suelta la tecla
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0
    
    # modificar ubicación del jugador    
    jugador_x += jugador_x_cambio   
    
    # mantener dentro de los bordes al jugador   
    if jugador_x <=0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x= 736
    
    # modificar ubicación del enemigo 
    for e in range(cantidad_enemigos):    
        #  fin del juego 
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        enemigo_x[e] += enemigo_x_cambio[e]   
    
    # mantener dentro de los bordes al enemigo   
        if enemigo_x[e] <=0:
            enemigo_x_cambio[e] = 1 # cambio de mov hacia la derecha
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -1 # cambio de mov hacia la izquierda  
            enemigo_y[e] += enemigo_y_cambio[e]
            
        # colisión 
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound('music/golpe.mp3')
            sonido_colision.set_volume(0.35)
            sonido_colision.play()
            bala_y=500
            bala_visible= False  
            puntaje +=1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)  
        enemigo(enemigo_x[e],enemigo_y[e],e) 
        
    # movimiento bala
    if bala_y<= -64:
        bala_y = 500
        bala_visible = False
        
    if bala_visible:
        disparar_bala(bala_x,bala_y)
        bala_y -= bala_y_cambio
    
    
    jugador(jugador_x,jugador_y) # pintar jugador
    mostrar_puntaje(texto_x,texto_y)
    #actualizar 
    pygame.display.update()
    