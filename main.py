import pygame
from constantes import *
import tablero

# Configuración inicial de pygame
pygame.init()
pantalla_juego = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('Los Simpsons Memotest')
clock_fps = pygame.time.Clock()  # Creamos un Clock para poder fijar los FPS

# Creamos eventos de tiempo
evento_1000ms = pygame.USEREVENT
pygame.time.set_timer(evento_1000ms, 1000)

# Configuracion inicial del juego
tablero_juego = tablero.crear_tablero()
cronometro = TIEMPO_JUEGO
cantidad_movimientos = CANTIDAD_INTENTOS
cantidad_tarjetas_cubiertas = CANTIDAD_TARJETAS_UNICAS * 2
cantidad_tarjetas_descubiertas = 0

#
img_game_over = pygame.image.load("{0}Game_Over.jpg".format(CARPETA_RECURSOS))
img_game_over_re = pygame.transform.scale(img_game_over, (1000, 1000))
img_start = pygame.image.load("{0}start.png".format(CARPETA_RECURSOS))
img_start_re = pygame.transform.scale(img_start, (125, 75))
rect_img_start = img_start_re.get_rect()
esta_corriendo = True


def terminar_partida(cronometro: int, cantidad_movimientos: int, tablero: dict):
    '''
    Verifico si el usuario ganó o perdio la partida
    si se queda sin movimientos o sin tiempo perdió 
    si todos las tarjetas del tablero están descubiertas el jugador gano
    Recibe el cronometro, los movimientos actuales del jugador y el tablero
    Si el jugador gano cambia la pantalla y muestra (VICTORIA O DERROTA DEPENDIENDO DE LO QUE HAYA PASADO)
    Retorna True si la partida termino y False si no lo terminó.
    '''
    lista_tarjetas = tablero["tarjetas"]
    lista_descubiertos = []
    for tarjeta_simpson in lista_tarjetas:
        if tarjeta_simpson["descubierto"] == True:
            lista_descubiertos.append(tarjeta_simpson)

    if len(lista_tarjetas) == len(lista_descubiertos):
        pantalla_juego.fill(COLOR_NEGRO)
        pantalla_juego.blit(img_game_over, (0,0))
        pantalla_juego.blit(img_start_re, (ANCHO_PANTALLA/2 -70, ALTO_PANTALLA/2))
        return True
    if cronometro <= 0 or cantidad_movimientos <= 0:
        pantalla_juego.fill(COLOR_NEGRO)
        pantalla_juego.blit(img_game_over, (0, 0))
        pantalla_juego.blit(img_start_re, (ANCHO_PANTALLA/2 -70, ALTO_PANTALLA/2))
        return False
    
    return None



while esta_corriendo:

    # Fijamos un valor de FPS
    clock_fps.tick(FPS)

    # Manejamos los eventos
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            esta_corriendo = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            print(pos)
            SONIDO_CLICK.play()
            if tablero.detectar_colision(tablero_juego, pos) != None:
                cantidad_movimientos -= 1
                SONIDO_VOLTEAR.play()

        # Cada vez que pase un segundo restamos uno al tiempo del cronometro
        if event.type == evento_1000ms:
            cronometro -= 1

    texto_cronometro = utils.generar_texto(
        "Arial Narrow", 15, str(cronometro), COLOR_NEGRO)
    texto_cantidad_intentos = utils.generar_texto(
        "Arial Narriw", 15, str(cantidad_movimientos), COLOR_NEGRO)
    tablero.actualizar_tablero(tablero_juego)

    # Dibujar pantalla
    pantalla_juego.fill(COLOR_BLANCO)  # Pintamos el fondo de color blanco
    # Verificamos si el juego termino
    # Pintamos el tiempo que falta para terminar la partida
    pantalla_juego.blit(texto_cronometro, (30, 560))

    # pantalla_juego.blit((5,100))
    
    # Pintamos el tiempo que falta para terminar la partida
    pantalla_juego.blit(texto_cantidad_intentos, (60, 560))
    tablero.dibujar_tablero(tablero_juego, pantalla_juego)

    terminar_partida(cronometro,cantidad_movimientos,tablero_juego)
    # Mostramos los cambios hechos
    pygame.display.flip()

pygame.quit()
