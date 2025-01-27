import pygame
import random
import math
pygame.init() # inicializar pygame 

# crear la pantalla
pantalla = pygame.display.set_mode((800,600))

# Titulo e icono 
pygame.display.set_caption("Invación espacial") # 32 px
icono = pygame.image.load("images/alien.png") # para cargarle imagenes
pygame.display.set_icon(icono)
fondo = pygame.image.load("images/galaxia_fondo.jpg")
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
img_enemigo = pygame.image.load("images/enemigo.png")
enemigo_x = random.randint(0, 736)
enemigo_y = random.randint(50, 200)
enemigo_x_cambio = 0.5
enemigo_y_cambio = 50

# Variable de la bala 
img_bala = pygame.image.load("images/bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

# puntaje 
puntaje = 0

#Funcion jugador 
def jugador(x,y):
    pantalla.blit(img_jugador, (x, y)) # arrojar (imagen, (posicionX,posicionY))

#Funcion jugador 
def enemigo(x,y):
    pantalla.blit(img_enemigo, (x, y)) # arrojar (imagen, (posicionX,posicionY))

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
    enemigo_x += enemigo_x_cambio   
    
    # mantener dentro de los bordes al enemigo   
    if enemigo_x <=0:
        enemigo_x_cambio = 1 # cambio de mov hacia la derecha
        enemigo_y += enemigo_y_cambio
    elif enemigo_x >= 736:
        enemigo_x_cambio = -1 # cambio de mov hacia la izquierda  
        enemigo_y += enemigo_y_cambio 
        
    # movimiento bala
    if bala_y<= -64:
        bala_y = 500
        bala_visible = False
        
    if bala_visible:
        disparar_bala(bala_x,bala_y)
        bala_y -= bala_y_cambio
    
    # colisión 
    colision = hay_colision(enemigo_x, enemigo_y, bala_x, bala_y)
    if colision:
        bala_y=500
        bala_visible= False  
        puntaje +=1
        print(puntaje)
        enemigo_x = random.randint(0, 736)
        enemigo_y = random.randint(50, 200)   
    jugador(jugador_x,jugador_y) # pintar jugador
    enemigo(enemigo_x,enemigo_y) 
    
    #actualizar 
    pygame.display.update()
    