from customtkinter import *
import simulacionFuego
import Utilidades
from PIL import Image
from tkinter import messagebox


class MainApp(CTk):

    # Configuración inicial de CustomTkinter
    set_appearance_mode("light")  # Modo oscuro
    set_default_color_theme("blue")  # Tema de color por defecto
    
    def __init__(self):
        super().__init__()
        self.title("Autómata Celular - Simulación de Incendios")
        self.geometry("1280x720")
        self.resizable(False, False)


        #Zona de Declaración de Parámetros importantes

        self.diccionarioValores = {}

        self.valoresMatrizViento = {}
        self.valoresMatrizAltura = {}

        
        self.combo_predeterminado = None

        self.ruta = None


  
        #Decoración y Fondo de app
        imagenFondo = Utilidades.icono(self, "FondoDegradadoMain", 1280, 720)
        imagenFondo.place(relx = 0, rely = 0, anchor = "nw")    

        frameBlancoFondo = CTkFrame(
            self,
            bg_color= "white",
            fg_color= "white",
            corner_radius=20,
            width=1200,
            height=600,
        )

        frameBlancoFondo.pack(expand = True)
        frameBlancoFondo.pack_propagate(False)


        panelUsuario = CTkFrame(
            frameBlancoFondo,
            fg_color= "transparent",
            height= 90                  
        )


        panelInformacion = CTkFrame(
            frameBlancoFondo,
            fg_color= "transparent",
            height= 510
                     
        )


        #Dividir la pantalla en 2 paneles distintos
        panelUsuario.pack(expand = True, fill = "x")
        panelUsuario.pack_propagate(False)
        panelInformacion.pack(expand = True, fill = "x")
        panelInformacion.pack_propagate(False)


        #Ícono para volver atrás
        iconBack = CTkImage(dark_image= Image.open("BackSymbol1.png"), size = (51,51))
        img_lab1 = CTkButton(panelUsuario, image=iconBack, text="", bg_color="white", fg_color="white", width=51, height=51, hover_color = "white", command=lambda: self.destroy())
        img_lab1.pack(side = "left", padx = 20)


        #Mensaje Principal de Ventana

        panelTitulo = CTkFrame(panelInformacion, fg_color = "transparent", corner_radius=16)
        panelTitulo.pack(fill = "x")

        textoPrincipal = Utilidades.bigText(panelTitulo,"Bienvenido al Sistema de Simulación de Incendios")
        textoPrincipal.pack(side = "left", padx = 50)

        subPanel = CTkFrame(panelInformacion, fg_color= "transparent", corner_radius=16)
        subPanel.pack(expand = True, fill = "both")
        



        #Subpaneles del panel de Información

        subPanel.rowconfigure(0, weight = 1)
        subPanel.columnconfigure(0, weight = 7)
        subPanel.columnconfigure(1, weight = 3)

        panelIzquierdo = CTkScrollableFrame(subPanel, fg_color= "#F2F2F2", corner_radius=16)
        panelIzquierdo.grid(row = 0, column = 0, sticky = "nswe", padx = 20, pady = 10)

        panelDerecho = CTkFrame(subPanel, fg_color= "#FC6161", corner_radius=16)
        panelDerecho.grid(row = 0, column = 1, sticky = "nswe", padx = 10, pady = 10)


        #Panel Izquierdo - Selección de Configuraciones para la Simulación

        configuraciones = Utilidades.bigText(panelIzquierdo, "Configuraciones")
        configuraciones.pack(anchor = "nw", padx = 5, pady = 10)

        matrizDeViento = Utilidades.mediumText(panelIzquierdo, "Matriz de Viento")
        matrizDeViento.pack(anchor = "nw", padx = 10, pady = 10)

        matrizDeVientoConfigurar = Utilidades.botonAccion(panelIzquierdo, "Configurar", 20, "verde", 180, 40, lambda: ventanaSobreVentanaViento())  
        matrizDeVientoConfigurar.pack(anchor = "nw", padx = 10, pady = 10)

        def ventanaSobreVentanaViento():
            nueva_Ventana = CTkToplevel(self)
            nueva_Ventana.title("Configurar Matriz de Viento")
           

            nueva_Ventana.rowconfigure(0, weight = 9)
            nueva_Ventana.rowconfigure(1, weight = 1)
            nueva_Ventana.columnconfigure(1, weight = 1)

            panelSuperior = CTkFrame(nueva_Ventana, fg_color= "white")
            panelSuperior.rowconfigure((0,1,2), weight = 1)
            panelSuperior.columnconfigure((0,1,2), weight = 1)
            panelSuperior.grid(row = 0, column = 0, sticky = "nsew")

            botonGuardar = Utilidades.botonAccion(nueva_Ventana, "Guardar Matriz de Viento", 20, "verde", 100, 35, lambda: obtener_valores())
            botonGuardar.grid(row = 1, column = 0)

            # Diccionario para almacenar las entradas
            entries = {}

            # Función para validar números de hasta 1 decimal
            def validar_entrada(texto):
                if texto == "" or texto == "-":
                    return True  # Permitir vacío o signo negativo inicial
                try:
                    valor = float(texto)
                    return len(texto.split(".")[-1]) <= 1  # Máximo 1 dígito decimal
                except ValueError:
                    return False

            # Crear entradas en cada celda
            for fila in range(3):  # 3 filas
                for columna in range(3):  # 3 columnas
                    # Crear un CTkEntry
                    validate_command = nueva_Ventana.register(validar_entrada)
                    entry = CTkEntry(
                        panelSuperior,
                        border_color="black",  # Borde negro
                        border_width=2,
                        font = ("Labrada", 50), 
                        justify = "center", 
                        placeholder_text="0",
                        validate="key",
                        validatecommand=(validate_command, "%P")                        
                    )
                    entry.grid(row=fila, column=columna, sticky="nsew", padx=2, pady=2)  # Ajustar tamaño y posición
                    # Guardar la entrada en el diccionario usando la posición como clave
                    entries[(fila, columna)] = entry
          
            

            # Función para obtener los valores de todas las entradas
            def obtener_valores():
            # Verificar si todas las entradas están llenas
                for (fila, columna), entry in entries.items():
                    valor = entry.get()
                    if valor.strip() == "":  # Si está vacío
                        messagebox.showerror("Error", "Todas las celdas deben estar llenas.")
                        return  # Detener el guardado

                    # Convertir coordenadas según el sistema y guardar el valor
                    self.valoresMatrizViento[(fila, columna)] = float(valor)
                
                # Si todo es válido, imprimir los valores                
                messagebox.showinfo("Éxito", "Matriz de viento guardada correctamente.")
                self.valoresMatrizViento[(1, 1)] = 0.0
                print("Valores de las entradas (transformados):", self.valoresMatrizViento)
                nueva_Ventana.destroy()

    

        matrizDeAlturas = Utilidades.mediumText(panelIzquierdo, "Matriz de Alturas")
        matrizDeAlturas.pack(anchor = "nw", padx = 10, pady = 10)

        matrizDeAlturasConfigurar = Utilidades.botonAccion(panelIzquierdo, "Configurar", 20, "verde", 180, 40, lambda: ventanaSobreVentanaAlturas())  
        matrizDeAlturasConfigurar.pack(anchor = "nw", padx = 10, pady = 10)    


        def ventanaSobreVentanaAlturas():
            nueva_Ventana = CTkToplevel(self)
            nueva_Ventana.title("Configurar Matriz de Alturas")
           

            nueva_Ventana.rowconfigure(0, weight = 9)
            nueva_Ventana.rowconfigure(1, weight = 1)
            nueva_Ventana.columnconfigure(1, weight = 1)

            panelSuperior = CTkFrame(nueva_Ventana, fg_color= "white")
            panelSuperior.rowconfigure((0,1,2), weight = 1)
            panelSuperior.columnconfigure((0,1,2), weight = 1)
            panelSuperior.grid(row = 0, column = 0, sticky = "nsew")

            botonGuardar = Utilidades.botonAccion(nueva_Ventana, "Guardar Matriz de Alturas", 20, "verde", 100, 35, lambda: obtener_valores())
            botonGuardar.grid(row = 1, column = 0)

            # Diccionario para almacenar las entradas
            entries = {}

            # Función para validar números de hasta 1 decimal
            def validar_entrada(texto):
                if texto == "" or texto == "-":
                    return True  # Permitir vacío o signo negativo inicial
                try:
                    valor = float(texto)
                    return len(texto.split(".")[-1]) <= 1  # Máximo 1 dígito decimal
                except ValueError:
                    return False

            # Crear entradas en cada celda
            for fila in range(3):  # 3 filas
                for columna in range(3):  # 3 columnas
                    # Crear un CTkEntry
                    validate_command = nueva_Ventana.register(validar_entrada)
                    entry = CTkEntry(
                        panelSuperior,
                        border_color="black",  # Borde negro
                        border_width=2,
                        font = ("Labrada", 50), 
                        justify = "center", 
                        placeholder_text="0",
                        validate="key",
                        validatecommand=(validate_command, "%P")                        
                    )
                    entry.grid(row=fila, column=columna, sticky="nsew", padx=2, pady=2)  # Ajustar tamaño y posición
                    # Guardar la entrada en el diccionario usando la posición como clave
                    entries[(fila, columna)] = entry

            # Función para obtener los valores de todas las entradas
            def obtener_valores():
            # Verificar si todas las entradas están llenas
                for (fila, columna), entry in entries.items():
                    valor = entry.get()
                    if valor.strip() == "":  # Si está vacío
                        messagebox.showerror("Error", "Todas las celdas deben estar llenas.")
                        return  # Detener el guardado

                    # Convertir coordenadas según el sistema y guardar el valor
                    self.valoresMatrizAltura[(fila, columna)] = float(valor)
                
                # Si todo es válido, imprimir los valores
                print("Valores de las entradas (transformados):", self.valoresMatrizAltura)
                messagebox.showinfo("Éxito", "Matriz de Altura guardada correctamente.")
                self.valoresMatrizAltura[(1, 1)] = 0.0
                nueva_Ventana.destroy()


        velocidad = Utilidades.mediumText(panelIzquierdo, "Velocidad del Viento")
        velocidad.pack(anchor = "nw", padx = 10, pady = 10)

        entradaVelocidad = CTkEntry(panelIzquierdo, width = 180, 
                    height = 50, 
                    corner_radius= 16, 
                    border_width=0, fg_color= "white", 
                    font = (("Labrada", 20)), 
                    justify = "left", 
                    placeholder_text="Valor...")
        entradaVelocidad.pack(anchor = "nw", padx = 10, pady = 10)

        densidadVegetacion = Utilidades.mediumText(panelIzquierdo, "Densidad de Vegetación")
        densidadVegetacion.pack(anchor = "nw", padx = 10, pady = 10)

        entradaDensidadVegetacion = CTkEntry(panelIzquierdo, width = 180, 
                    height = 50, 
                    corner_radius= 16, 
                    border_width=0, fg_color= "white", 
                    font = (("Labrada", 20)), 
                    justify = "left", 
                    placeholder_text="Valor...")
        entradaDensidadVegetacion.pack(anchor = "nw", padx = 10, pady = 10)



    
        

        mapaInicial = Utilidades.mediumText(panelIzquierdo, "Mapa Inicial")
        mapaInicial.pack(anchor = "nw", padx = 10, pady = 10)


        # Lista inicial para el ComboBox de los mapas predeterminados
        opciones_mapas = ["Amazonía - Manaos", "Canadá - Québec", "Grecia - Evros"]

        
    
        
        # Función para manejar los cambios en el ComboBox principal
        def manejar_cambio(opcion_seleccionada):
            # Eliminar widgets anteriores (si los hay)
            for widget in frame_dinamico.winfo_children():
                widget.destroy()

            # Evitar que se dispare el evento al seleccionar el "placeholder"
            if opcion_seleccionada == "Seleccionar...":
                frame_dinamico.pack_forget()
                return

            frame_dinamico.pack(pady=20, fill="both", expand=True)

            # Mostrar contenido según la opción seleccionada
            if opcion_seleccionada == "Predeterminado":
                # Crear un nuevo ComboBox con las opciones predeterminadas
                self.combo_predeterminado = CTkComboBox(
                    frame_dinamico,
                    values=opciones_mapas,
                    state = "readonly"
                )
                self.combo_predeterminado.set("Seleccionar valor...")
                self.combo_predeterminado.pack(side = "left", padx = 20, pady = 5)

            elif opcion_seleccionada == "Customizado":
                # Crear un botón para customizar el mapa
                boton_customizar = Utilidades.botonAccion(
                    frame_dinamico,
                    "Customizar Mapa",
                    20,
                    "verde",
                    360,
                    35,
                    lambda: None
                )
                boton_customizar.pack(side = "left", padx = 20, pady = 5)

            elif opcion_seleccionada == "Imagen":
                # Crear un botón para subir una imagen
                boton_imagen = Utilidades.botonAccion(
                    frame_dinamico,
                    "Subir Imagen",
                    20,
                    "verde",
                    360,
                    35,
                    lambda: seleccionar_archivo()

                )
                boton_imagen.pack(side = "left", padx = 20, pady = 5)

                def seleccionar_archivo():
                    # Abrir el explorador de archivos
                    ruta_archivo = filedialog.askopenfilename(
                        title="Seleccionar archivo",
                        filetypes=[("Todos los archivos", "*.*"), ("PDF Files", "*.pdf"), ("Imágenes", "*.jpg;*.png;*.jpeg")]
                    )

                    if ruta_archivo:  # Verificar si se seleccionó un archivo
                        self.ruta = ruta_archivo
                        print(f"Archivo seleccionado: {self.ruta}")
                        messagebox.showinfo("Archivo Seleccionado", f"Archivo seleccionado:\n{self.ruta}")

        # Crear el ComboBox principal
        opciones_principales = ["Seleccionar...", "Predeterminado", "Customizado", "Imagen"]
        combo_principal = CTkComboBox(
            panelIzquierdo,
            values=opciones_principales,
            state = "readonly",
            command= manejar_cambio  # Vincular función al cambio de selección
        )
        combo_principal.set("Seleccionar...")  # Configurar el texto inicial como placeholder
        combo_principal.pack(anchor = "nw", padx = 10, pady = 10)

        # Frame dinámico donde aparecerán los widgets según la selección
        frame_dinamico = CTkFrame(panelIzquierdo, fg_color = "transparent")
        frame_dinamico.pack_forget()




        #Panel Derecho - Botón para iniciar la simulación en una nueva ventana con la ayuda de Pygame


        botonIniciar = Utilidades.botonAccion(panelDerecho, "Iniciar Simulación", 40, "#FC6161", 3, 3, lambda: iniciarJuego())
        botonIniciar.configure(hover = False)
        botonIniciar.pack(expand = True )

        def iniciarJuego():


            #Comprobación de cuáles campos están vacíos y cuáles no, y asignación de sus valores al diccionario para mandarlos comoa argumento

            if not self.valoresMatrizViento:        #Matriz Vacía
                for fila in range(3):  # 3 filas
                    for columna in range(3):
                        self.valoresMatrizViento[(columna - 1, 1 - fila)] = 0

                self.diccionarioValores["matrizViento"] = self.valoresMatrizViento

            else: self.diccionarioValores["matrizViento"] = self.valoresMatrizViento
                

            if not self.valoresMatrizAltura:        #Matriz Vacía
                for fila in range(3):  # 3 filas
                    for columna in range(3):
                        self.valoresMatrizAltura[(columna - 1, 1 - fila)] = 0

                self.diccionarioValores["matrizAltura"] = self.valoresMatrizAltura

            else: self.diccionarioValores["matrizAltura"] = self.valoresMatrizAltura

            if entradaVelocidad.get() == "":
                self.diccionarioValores["velocidad"] = 0
            else:
                self.diccionarioValores["velocidad"] = float(entradaVelocidad.get())

            if entradaDensidadVegetacion.get() == "":
                self.diccionarioValores["densidadVegetacion"] = 0
            else:
                self.diccionarioValores["densidadVegetacion"] = float(entradaDensidadVegetacion.get())


            if combo_principal.get() == "Predeterminado":

                if self.combo_predeterminado.get() == "Amazonía - Manaos":

                    simulacion = simulacionFuego.ejecutarSimulacion(self.diccionarioValores)
                    matrizImagen = simulacion.procesar_imagen_a_matriz("amazonia_manaos.png", 500, 500)
                    simulacion.iniciar_juego(matrizImagen)

                elif self.combo_predeterminado.get() == "Canadá - Québec":

                    simulacion = simulacionFuego.ejecutarSimulacion(self.diccionarioValores)
                    matrizImagen = simulacion.procesar_imagen_a_matriz("quebec_canada.png", 500, 500)
                    simulacion.iniciar_juego(matrizImagen)

                elif self.combo_predeterminado.get() == "Grecia - Evros":

                    simulacion = simulacionFuego.ejecutarSimulacion(self.diccionarioValores)
                    matrizImagen = simulacion.procesar_imagen_a_matriz("evros_grecia.png", 500, 500)
                    simulacion.iniciar_juego(matrizImagen)
          
                
                

            elif combo_principal.get() == "Customizado":

                print("xd")

            elif combo_principal.get() == "Imagen":

                if self.ruta != None:

                    simulacion = simulacionFuego.ejecutarSimulacion(self.diccionarioValores)
                    matrizImagen = simulacion.procesar_imagen_a_matriz(self.ruta, 500, 500)
                    simulacion.iniciar_juego(matrizImagen)
    
      
    

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()





