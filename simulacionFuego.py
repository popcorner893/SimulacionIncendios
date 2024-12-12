import pygame
import random

from PIL import Image
import numpy as np

class ejecutarSimulacion:

    def __init__(self, diccionarioParámetros):
        
        self.diccionarioParámetros = diccionarioParámetros

        self.valores_categoria = {
        "Bosque": 0,
        "Carretera": 1,
        "Ríos": 2,
        "Ciudad": 3
        }

    
    # Función principal para procesar la imagen
    def procesar_imagen_a_matriz(self, ruta_imagen, ancho, alto):
        # Función para clasificar un píxel según los criterios especificados
        def clasificar_pixel(pixel):
            r, g, b = pixel
            if g > b and g >= 230 and r < 230:  # Bosque
                return "Bosque" 
            elif b > g and b >= 230:  # Ríos
                return "Ríos"
            elif r >= 230 and g >= 230 and b >= 220:  # Ciudad
                return "Ciudad"
            else:  # Carreteras
                return "Carretera"

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
            print("propagando")
            new_tablero = [fila[:] for fila in tablero]  # Crear una copia del tablero
            for fila in range(FILAS):
                for columna in range(COLUMNAS):
                    if tablero[fila][columna]['estado']  == 1:  # Si la celda está en fuego
                        # Quemar la celda actual
                        new_tablero[fila][columna]['estado'] = 2
                        # Propagar el fuego a las casillas vecinas
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1,-1), (1,1), (-1,1), (1,-1)]:
                            nr, nc = fila + dr, columna + dc
                            if 0 <= nr < FILAS and 0 <= nc < COLUMNAS and tablero[nr][nc]['estado'] == 0 and tablero[nr][nc]['tipo']=='bosque':
                                if random.random() < calcularPropagacion(dr,dc,fila,columna):  # Probabilidad de propagación
                                    new_tablero[nr][nc]['estado'] = 1
            
            return new_tablero
        

        def calcularPropagacion(dr, dc, fila, columna):
            #calculo de angulo entre vector viento y la direccion de propagacion
            probabilidad=0.1
            vectorPropagacion = np.array([dr, -dc])
            print(self.diccionarioParámetros["matrizViento"])
            vectorViento =  calcular_vector_general(self.diccionarioParámetros["matrizViento"])
            productoPunto = np.dot(vectorViento, vectorPropagacion)
            norma_viento = np.linalg.norm(vectorViento)
            norma_propagacion = np.linalg.norm(vectorPropagacion)
            angulo_entre_viento_propagacion = np.arccos(np.clip(productoPunto / (norma_viento * norma_propagacion), -1.0, 1.0))
            
            if angulo_entre_viento_propagacion <= np.pi/6:
                probabilidad+=(self.diccionarioParámetros["velocidad"]/10)
            elif(angulo_entre_viento_propagacion <= 2*np.pi/3):
                probabilidad+=(self.diccionarioParámetros["velocidad"]/30)
            else:
                probabilidad -= (self.diccionarioParámetros["velocidad"]/30)
                
                
            pendiente = calcular_vector_pendiente(self.diccionarioParámetros["matrizAltura"])
            if np.linalg.norm(pendiente+vectorPropagacion) > 0:  # Subiendo
                probabilidad += (self.diccionarioParámetros["densidadVegetacion"]/30)
            elif np.linalg.norm(pendiente+vectorPropagacion) < 0:  # Bajando
                probabilidad -= (self.diccionarioParámetros["densidadVegetacion"]/30)
            else:
                probabilidad += (self.diccionarioParámetros["densidadVegetacion"])
                
            return probabilidad


        def calcular_vector_general(matriz_viento):
        # Matriz auxiliar que define los desplazamientos relativos
        
            # Obtener el tamaño de la matriz (en este caso es 3x3)
            filas = max(key[0] for key in matriz_viento.keys()) + 1
            columnas = max(key[1] for key in matriz_viento.keys()) + 1

            # Crear la matriz vacía
            matriz = [[0] * columnas for _ in range(filas)]

            # Llenar la matriz con los valores del diccionario
            for (fila, columna), valor in matriz_viento.items():
                matriz[fila][columna] = valor

            
            desplazamientos = np.array([
                [(-1, -1), (-1, 0), (-1, 1)],
                [(0, -1), (0, 0), (0, 1)],
                [(1, -1), (1, 0), (1, 1)]
            ])
            
            # Inicializar el vector resultante
            vector_x, vector_y = 0, 0
            
            # Recorrer la matriz y calcular el vector ponderado
            for i in range(3):
                for j in range(3):
                    if matriz[i][j] == 1:  # Solo considerar celdas con viento
                        vector_x += desplazamientos[i, j][0]
                        vector_y += desplazamientos[i, j][1]
            
            # Normalizar el vector resultante (opcional)
            magnitud = np.sqrt(vector_x**2 + vector_y**2)
            if magnitud > 0:
                vector_x /= magnitud
                vector_y /= magnitud
            return (vector_x, vector_y)
            

        def calcular_vector_pendiente(matriz_altura):
            
            # Obtener el tamaño de la matriz (en este caso es 3x3)
            filas = max(key[0] for key in matriz_altura.keys()) + 1
            columnas = max(key[1] for key in matriz_altura.keys()) + 1

            # Crear la matriz vacía
            matriz = [[0] * columnas for _ in range(filas)]

            # Llenar la matriz con los valores del diccionario
            for (fila, columna), valor in matriz_altura.items():
                matriz[fila][columna] = valor
            
            # Matriz auxiliar de desplazamientos
            desplazamientos = np.array([
                [(-1, -1), (-1, 0), (-1, 1)],
                [(0, -1), (0, 0), (0, 1)],
                [(1, -1), (1, 0), (1, 1)]
            ])
            
            # Inicializar el vector resultante
            vector_x, vector_y = 0, 0
            filas, columnas = len(matriz), len(matriz[0])
            
            for i in range(1, filas - 1):  # Evitamos los bordes
                for j in range(1, columnas - 1):
                    for k in range(3):  # Filas de la ventana 3x3
                        for l in range(3):  # Columnas de la ventana 3x3
                            di, dj = desplazamientos[k][l]
                            ni, nj = i + di, j + dj
                            
                            if 0 <= ni < filas and 0 <= nj < columnas:
                                pendiente = matriz[ni][nj] - matriz[i][j]
                                vector_x += pendiente * di
                                vector_y += pendiente * dj
            
            # Normalizar el vector
            magnitud = np.sqrt(vector_x**2 + vector_y**2)
            if magnitud > 0:
                vector_x /= magnitud
                vector_y /= magnitud
            
            return (vector_x, -vector_y)

        
        # fila_central = random.randint(0, FILAS - 1)
        # columna_central = random.randint(0, COLUMNAS - 1)

        #Celda inicial del incendio
        # while tablero[fila_central][columna_central]["tipo"] != "bosque":
        #     fila_central = random.randint(0, FILAS - 1)
        #     columna_central = random.randint(0, COLUMNAS - 1)
        tablero[FILAS-1][COLUMNAS-1]["estado"] = 1

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

            pygame.time.wait(50)

        # Cerrar Pygame
        pygame.quit()
        


# tablero = [[0 for _ in range(300)] for _ in range(300)]
# Alturas = [[1 for _ in range(300)] for _ in range(300)]
# vientos = [[(1,1) for _ in range(200)] for _ in range(200)]
# densidadForestal = 1
# diccionarioParámetros = {
#     "matrizViento": vientos,
#     "matrizAltura": Alturas,
#     "densidadBosque": densidadForestal
# }
# matriz = [[0 for _ in range(200)] for _ in range(200)]
# juego = ejecutarSimulacion(diccionarioParámetros)
# juego.iniciar_juego(matriz)
        