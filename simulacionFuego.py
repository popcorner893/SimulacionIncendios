import pygame
import random

class ejecutarSimulacion:

    def iniciar_juego():

        # Configuración inicial
        ANCHO, ALTO = 800, 800  # Tamaño de la ventana
        FILAS, COLUMNAS = 100, 100  # Dimensiones del tablero
        TAMANO_CELDA = ANCHO // COLUMNAS  # Tamaño de cada celda

        # Colores
        COLOR_PREDETERMINADO = (34, 139, 34)  # Verde para casillas intactas
        COLOR_FUEGO = (255, 69, 0)  # Rojo para fuego
        COLOR_QUEMADO = (50, 50, 50)  # Gris para quemado

        # Inicializar Pygame
        pygame.init()
        pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Simulación de Propagación de Fuego - Pygame")

        # Inicializar el tablero (0: intacto, 1: en fuego, 2: quemado)
        tablero = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]

        # Función para dibujar el tablero
        def dibujar_tablero():
            for fila in range(FILAS):
                for columna in range(COLUMNAS):
                    color = COLOR_PREDETERMINADO if tablero[fila][columna] == 0 else \
                            COLOR_FUEGO if tablero[fila][columna] == 1 else \
                            COLOR_QUEMADO
                    pygame.draw.rect(pantalla, color, (columna * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))

        # Función para actualizar el estado del fuego
        def propagar():
            new_tablero = [fila[:] for fila in tablero]  # Crear una copia del tablero
            for fila in range(FILAS):
                for columna in range(COLUMNAS):
                    if tablero[fila][columna] == 1:  # Si la celda está en fuego
                        # Quemar la celda actual
                        new_tablero[fila][columna] = 2
                        # Propagar el fuego a las casillas vecinas
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1,-1), (1,1), (-1,1), (1,-1)]:
                            nr, nc = fila + dr, columna + dc
                            if 0 <= nr < FILAS and 0 <= nc < COLUMNAS and tablero[nr][nc] == 0:
                                if random.random() < 0.3:  # Probabilidad de propagación
                                    new_tablero[nr][nc] = 1
            return new_tablero

        # Iniciar el fuego en una posición central
        tablero[FILAS // 2][COLUMNAS // 2] = 1

        # Bucle principal
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Actualizar el tablero
            tablero = propagar()
            
            # Dibujar el tablero
            pantalla.fill((0, 0, 0))  # Limpiar la pantalla
            dibujar_tablero()
            pygame.display.flip()  # Actualizar la pantalla


            pygame.time.wait(1000)

        # Cerrar Pygame
        pygame.quit()