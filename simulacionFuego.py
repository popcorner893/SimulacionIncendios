import pygame
import random

from PIL import Image
import numpy as np

class ejecutarSimulacion:

    def __init__(self, diccionarioParámetros):
        
        self.diccionarioParámetros = diccionarioParámetros

        self.colores_representativos = {
        "Bosque": (175,239,202),   # #D3F8E2
        "Carretera": (139, 165, 193),  # #8BA5C1
        "Ríos": (144, 218, 238),     # #90DAEE
        "Ciudad": (245, 240, 229)    # #F5F0E5
        }

        self.valores_categoria = {
        "Bosque": 0,
        "Carretera": 1,
        "Ríos": 2,
        "Ciudad": 3
        }

    

    # Función principal para procesar la imagen
    def procesar_imagen_a_matriz(self,ruta_imagen, ancho, alto):
        
        # Función para calcular la distancia euclidiana en el espacio RGB
        def distancia_rgb(pixel, color_representativo):
            return np.sqrt(sum((p - c) ** 2 for p, c in zip(pixel, color_representativo)))

        # Función para clasificar un píxel según el color más cercano
        def clasificar_pixel(pixel):
            distancias = {categoria: distancia_rgb(pixel, color) for categoria, color in self.colores_representativos.items()}
            return min(distancias, key=distancias.get)  # Devolver la categoría con menor distancia

        # Cargar la imagen
        imagen = Image.open(ruta_imagen)
        
        # Redimensionar la imagen al tamaño deseado
        imagen = imagen.resize((ancho, alto))
        
        # Convertir la imagen a un array de píxeles RGB
        pixeles = np.array(imagen)
        
        # Crear una matriz para almacenar las categorías
        matriz_categorias = np.zeros((alto, ancho), dtype=int)
        
        # Clasificar cada píxel y asignarlo a la matriz
        for y in range(alto):
            for x in range(ancho):
                pixel = pixeles[y, x][:3]  # Ignorar canal alfa si existe
                categoria = clasificar_pixel(pixel)
                matriz_categorias[y, x] = self.valores_categoria[categoria]

        
        
        return matriz_categorias

    def inicializar_tablero_desde_matriz(self, matriz):
        # Crear el tablero basado en la matriz categorizada
        filas = len(matriz)
        columnas = len(matriz[0])
        tablero = [[{"estado": 0, "tipo": None, "propaga": True} for _ in range(columnas)] for _ in range(filas)]
        
        for fila in range(filas):
            for columna in range(columnas):
                tipo = matriz[fila][columna]
                if tipo == 0:  # Bosque
                    tablero[fila][columna]["tipo"] = "bosque"
                elif tipo == 1:  # Carretera
                    tablero[fila][columna]["tipo"] = "carretera"
                    tablero[fila][columna]["propaga"] = False
                elif tipo == 2:  # Ríos
                    tablero[fila][columna]["tipo"] = "río"
                    tablero[fila][columna]["propaga"] = False
                elif tipo == 3:  # Ciudad
                    tablero[fila][columna]["tipo"] = "ciudad"
        return tablero

    def iniciar_juego(self, matriz):
        # Configuración inicial
        ANCHO, ALTO = 500, 500  # Tamaño de la ventana
        FILAS, COLUMNAS = len(matriz), len(matriz[0])  # Dimensiones del tablero
        TAMANO_CELDA = ANCHO // COLUMNAS  # Tamaño de cada celda

        # Colores
        COLOR_BOSQUE = (34, 139, 34)
        COLOR_CARRETERA = (139, 165, 193)
        COLOR_RIO = (30, 144, 255)
        COLOR_CIUDAD = (245, 240, 229)
        COLOR_FUEGO = (255, 69, 0)
        COLOR_QUEMADO = (50, 50, 50)

        # Inicializar Pygame
        pygame.init()
        pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Simulación de Propagación de Fuego - Pygame")

        # Inicializar fuente para texto
        pygame.font.init()
        fuente = pygame.font.Font(None, 30)  # Tamaño 30, fuente predeterminada

        # Inicializar el tablero con la matriz
        tablero = self.inicializar_tablero_desde_matriz(matriz)

        # Contador de iteraciones
        iteracion = 0

        # Función para dibujar el tablero
        def dibujar_tablero():
            for fila in range(FILAS):
                for columna in range(COLUMNAS):
                    celda = tablero[fila][columna]
                    if celda["estado"] == 0:
                        color = COLOR_BOSQUE if celda["tipo"] == "bosque" else \
                                COLOR_CARRETERA if celda["tipo"] == "carretera" else \
                                COLOR_RIO if celda["tipo"] == "río" else \
                                COLOR_CIUDAD if celda["tipo"] == "ciudad" else \
                                (255,0,0)
                    elif celda["estado"] == 1:
                        color = COLOR_FUEGO
                    else:
                        color = COLOR_QUEMADO
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
                                if random.random() < calcularPropagacion(dr,dc,fila,columna):  # Probabilidad de propagación
                                    new_tablero[nr][nc] = 1
            return new_tablero
        

        def calcularPropagacion(dr, dc, fila, columna):
            #calculo de angulo entre vector viento y la direccion de propagacion
            probabilidad=0.2
            vectorPropagacion = np.array([dr, dc])
            vectorViento =  np.array(self.diccionarioParámetros["matrizViento"][(fila,columna)])
            productoPunto = np.dot(vectorViento, vectorPropagacion)
            print(vectorPropagacion)
            print(vectorViento)
            print(productoPunto)
            norma_viento = np.linalg.norm(vectorViento)
            print(norma_viento)
            norma_propagacion = np.linalg.norm(vectorPropagacion)
            print(norma_propagacion)
            angulo_entre_viento_propagacion = np.arccos(np.clip(productoPunto / (norma_viento * norma_propagacion), -1.0, 1.0))
            print(angulo_entre_viento_propagacion)
            
            if angulo_entre_viento_propagacion <= np.pi/6:
                probabilidad+=0.3
            elif(angulo_entre_viento_propagacion <= 2*np.pi/3):
                probabilidad+=0.1
            else:
                probabilidad = probabilidad -0.1
            if(self.diccionarioParámetros["matrizAltura"][(dr,dc)]-self.diccionarioParámetros["matrizAltura"][(fila,columna)]>0):
                probabilidad+=0.1
            elif(self.diccionarioParámetros["matrizAltura"][(dr,dc)]-self.diccionarioParámetros["matrizAltura"][(fila,columna)]<0):
                probabilidad-=0.1
            
            return probabilidad

        # Iniciar el fuego en una posición central
        tablero[(FILAS // 2)][COLUMNAS // 2]["estado"] = 1

        # Bucle principal
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            #Incrementar el número de iteración
            iteracion+=1

            # Actualizar el tablero
            tablero = propagar()

            # Dibujar el tablero
            pantalla.fill((0, 0, 0))  # Limpiar la pantalla
            dibujar_tablero()

            # Renderizar el texto con el número de iteración
            texto_iteracion = fuente.render(f"Iteración: {iteracion}", True, (255, 255, 255))  # Texto blanco
            pantalla.blit(texto_iteracion, (10, 10))  # Dibujar en la esquina superior izquierda

            pygame.display.flip()  # Actualizar la pantalla

            pygame.time.wait(1000)

        # Cerrar Pygame
        pygame.quit()
