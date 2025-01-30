import pygame
import random
import math
from pygame import mixer

pygame.init() # inicializar pygame 

# crear la pantalla
pantalla = pygame.display.set_mode((800,600))

# Titulo e icono 
pygame.display.set_caption("Invasión espacial") # 32 px
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
    enemigo_x_cambio.append(2) # velocidad de los enemigos
    enemigo_y_cambio.append(50)

# variable explosion
img_explosion = pygame.image.load("images/explosion.png")


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

# Función para mostrar el texto final
def texto_final():
    imagen_final = pygame.image.load("images/gameover.png") 
    pantalla.blit(imagen_final, (150, 150))
    # Mostrar opciones
    opcion_volver = fuente.render("Presiona ESPACIO para volver al menú", True, (255, 255, 255))
    opcion_salir = fuente.render("Presiona ESC para salir", True, (255, 255, 255))
    pantalla.blit(opcion_volver, (115, 300))
    pantalla.blit(opcion_salir, (115, 350))

    # Actualizar la pantalla
    pygame.display.update()

    # Esperar a que el usuario presione una tecla
    esperando_input = True
    while esperando_input:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:  # ENTER para volver al menú
                    return "menu"
                if evento.key == pygame.K_ESCAPE:  # ESC Para salir
                    return "salir"


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
    # Cargar la imagen del menú
    imagen_menu = pygame.image.load("images/fondomenu.jpg")  # Asegúrate de tener una imagen llamada "menu.png" en la carpeta "images"
    
    # Mostrar la imagen en la pantalla
    pantalla.blit(imagen_menu, (0, 0))  # La imagen se dibuja en la posición (0, 0)
# Loop del menú inicial
def loop_menu():
    en_menu = True
    while en_menu:
        pantalla.blit(fondo, (0, 0))
        mostrar_menu()
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return "jugar"
                if evento.key == pygame.K_ESCAPE:
                    return "salir"

#Loop del juego 

# Función para manejar el juego principal
def loop_juego():
    global jugador_x, jugador_y, jugador_x_cambio, bala_x, bala_y, bala_visible, puntaje

    # Variables para manejar explosiones
    explosion_activa = [False] * cantidad_enemigos
    explosion_timer = [0] * cantidad_enemigos

    se_ejecuta = True
    while se_ejecuta:
        pantalla.blit(fondo, (0, 0))

        # Iterar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jugador_x_cambio = -1
                if evento.key == pygame.K_RIGHT:
                    jugador_x_cambio = 1
                if evento.key == pygame.K_SPACE:
                    sonido_bala = mixer.Sound('music/disparo.mp3')
                    sonido_bala.set_volume(0.35)
                    sonido_bala.play()
                    if not bala_visible:
                        bala_x = jugador_x
                        disparar_bala(bala_x, bala_y)
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    jugador_x_cambio = 0

        # Modificar ubicación del jugador
        jugador_x += jugador_x_cambio

        # Mantener dentro de los bordes al jugador
        if jugador_x <= 0:
            jugador_x = 0
        elif jugador_x >= 736:
            jugador_x = 736

        # Modificar ubicación del enemigo
        for e in range(cantidad_enemigos):
            if explosion_activa[e]:
                # Mostrar la explosión
                pantalla.blit(img_explosion, (enemigo_x[e], enemigo_y[e]))

                # Verificar si han pasado 500ms desde que inició la explosión
                if pygame.time.get_ticks() - explosion_timer[e] > 500:
                    explosion_activa[e] = False
                    enemigo_x[e] = random.randint(0, 736)
                    enemigo_y[e] = random.randint(50, 200)
            else:
                # Fin del juego si un enemigo toca al jugador
                if hay_colision(jugador_x, jugador_y, enemigo_x[e], enemigo_y[e]):
                    for k in range(cantidad_enemigos):
                        enemigo_y[k] = 1000  # Mover a los enemigos fuera de la pantalla
                    opcion = texto_final()  # Mostrar pantalla de "GAME OVER" y esperar input

                    if opcion == "menu":
                        # Reiniciar variables del juego
                        jugador_x = 368
                        jugador_y = 500
                        puntaje = 0
                        bala_visible = False
                        for e in range(cantidad_enemigos):
                            enemigo_x[e] = random.randint(0, 736)
                            enemigo_y[e] = random.randint(50, 200)
                        return "menu"
                    elif opcion == "salir":
                        return "salir"

                enemigo_x[e] += enemigo_x_cambio[e]

                # Mantener dentro de los bordes al enemigo
                if enemigo_x[e] <= 0:
                    enemigo_x_cambio[e] = 1
                    enemigo_y[e] += enemigo_y_cambio[e]
                elif enemigo_x[e] >= 736:
                    enemigo_x_cambio[e] = -1
                    enemigo_y[e] += enemigo_y_cambio[e]

                # Colisión entre bala y enemigo
                colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
                if colision:
                    sonido_colision = mixer.Sound('music/golpe.mp3')
                    sonido_colision.set_volume(0.35)
                    sonido_colision.play()
                    bala_y = 500
                    bala_visible = False
                    puntaje += 1

                    # Activar la explosión
                    explosion_activa[e] = True
                    explosion_timer[e] = pygame.time.get_ticks()

                enemigo(enemigo_x[e], enemigo_y[e], e)

        # Movimiento de la bala
        if bala_y <= -64:
            bala_y = 500
            bala_visible = False

        if bala_visible:
            disparar_bala(bala_x, bala_y)
            bala_y -= bala_y_cambio

        jugador(jugador_x, jugador_y)
        mostrar_puntaje(texto_x, texto_y)
        pygame.display.update()
        
# Función principal para manejar el flujo del juego
def main():
    while True:
        opcion = loop_menu()
        if opcion == "salir":
            break
        elif opcion == "jugar":
            opcion = loop_juego()
            if opcion == "salir":
                break

# Ejecutar el juego
main()    
pygame.quit()