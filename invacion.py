import pygame
import random

pygame.init() # inicializar pygame 

# crear la pantalla
pantalla = pygame.display.set_mode((800,600))

# Titulo e icono 
pygame.display.set_caption("Invación espacial") # 32 px
icono = pygame.image.load("images/alien.png") # para cargarle imagenes
pygame.display.set_icon(icono)

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
jugador_y = 536
jugador_x_cambio = 0


# Variable de enemigo
img_enemigo = pygame.image.load("images/enemigo.png")
enemigo_x = random.randint(0, 736)
enemigo_y = random.randint(50, 200)
enemigo_x_cambio = 0.3
enemigo_y_cambio = 50




#Funcion jugador 
def jugador(x,y):
    pantalla.blit(img_jugador, (x, y)) # arrojar (imagen, (posicionX,posicionY))

#Funcion jugador 
def enemigo(x,y):
    pantalla.blit(img_enemigo, (x, y)) # arrojar (imagen, (posicionX,posicionY))



#Loop del juego 
se_ejecuta = True
while se_ejecuta == True :
    pantalla.fill((205, 144, 228)) # color relleno RGB (pintar color pantalla)
    # iterar eventos
    for evento in pygame.event.get():
        # evento cerrar programa
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        # evento presionar flechas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.3
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.3
        # evento soltar flechas    
        if evento.type == pygame.KEYUP: # Suelta la tecla
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0
    
    # modificar ubicación del jugador    
    jugador_x += jugador_x_cambio   
    
    # mantener dentro de los bordes al jugador   
    if jugador_x <=0:
        jugador_x = 0
    if jugador_x >= 736:
        jugador_x= 736
        
    jugador(jugador_x,jugador_y) # pintar jugador
    enemigo(enemigo_x,enemigo_y) 
    
    #actualizar 
    pygame.display.update()
    