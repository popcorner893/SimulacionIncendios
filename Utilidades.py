from customtkinter import *
from PIL import Image
import tkinter as tk
from tkcalendar import DateEntry
import re
from tkinter import StringVar

class tinyText(CTkLabel):

    def __init__(self, parent, texto):
        
        super().__init__(parent, text = texto, font=("Labrada", 20)) 


class smallText(CTkLabel):

    def __init__(self, parent, texto):
        
        super().__init__(parent, text = texto, font=("Labrada", 25))


class mediumText(CTkLabel):

    def __init__(self, parent, texto):
        
        super().__init__(parent, text = texto, font=("Labrada", 33)) 


class bigText(CTkLabel):

    def __init__(self, parent, texto):
        
        super().__init__(parent, text = texto, font=("Labrada", 40))     


class botonAccion(CTkButton):

    def __init__(self, parent, texto, tamano_texto, colorFondo, ancho, alto, comando):
        
        if colorFondo == "verde":               
        
            super().__init__(parent, text = texto,corner_radius=16, font=("Labrada", tamano_texto), fg_color= "#02E1B5", bg_color= "transparent", text_color= "black",width= ancho, height=alto, command=comando)

        elif colorFondo == "blanco":

            super().__init__(parent, text = texto,corner_radius=16, font=("Labrada", tamano_texto), fg_color= "white", bg_color= "transparent", text_color= "black",width= ancho, height=alto, command=comando)

        else:

            super().__init__(parent, text = texto,corner_radius=16, font=("Labrada", tamano_texto), fg_color= "#FF6666", bg_color= "transparent", text_color= "black",width= ancho, height=alto, command=comando)


class icono(CTkLabel):

    def __init__(self, parent, direccion, ancho, alto):
        
        imagen = CTkImage(dark_image= Image.open(f"{direccion}.png"), size = (ancho,alto))
        super().__init__(parent, image = imagen, text = "")  

class iconoClickable(CTkButton):
        
    def __init__(self, parent, direccion, ancho, alto, comando):
        
        imagen = CTkImage(dark_image= Image.open(f"{direccion}.png"), size = (ancho,alto))

        super().__init__(parent, image = imagen, text = "", bg_color="transparent", fg_color="transparent", width=ancho, height=alto, command= comando, hover_color="white")  



class entradaFecha(CTkFrame):


    
    def __init__(self, parent, texto_fecha):
        super().__init__(parent, fg_color="transparent", corner_radius=16)

        self.fecha_seleccionada = None  # Para guardar la fecha seleccionada

        # Etiqueta para mostrar texto inicial
        self.label = smallText(self, texto_fecha)
        self.label.pack(side="left", padx=10)

        # Botón para abrir el calendario
        self.seleccionarFecha = botonAccion(self, "", 20, "blanco", 180, 50, lambda: self.abrir_calendario())
        self.seleccionarFecha.pack(side="left", padx=5)

        #Icono

        self.icono = icono(self, "calendarIcon1", 42, 42)
        self.icono.pack(side = "left")

    def abrir_calendario(self):
        # Crear ventana emergente
        self.ventana_calendario = CTkToplevel(self)
        self.ventana_calendario.title("Seleccionar Fecha")
        self.ventana_calendario.geometry("300x200")
        self.ventana_calendario.grab_set()  # Bloquear interacción con la ventana principal

        # Crear widget de calendario
        self.calendario = DateEntry(
            self.ventana_calendario,
            background='darkblue',
            foreground='white',
            date_pattern='dd/mm/yyyy',
            width=15
        )
        self.calendario.pack(pady=10)

        # Botón para confirmar la selección
        boton_confirmar = CTkButton(
            self.ventana_calendario,
            text="Confirmar",
            command=self.obtener_fecha
        )
        boton_confirmar.pack(pady=10)

    def obtener_fecha(self):
        # Obtener la fecha seleccionada y actualizar la etiqueta
        self.fecha_seleccionada = self.calendario.get_date()
        self.seleccionarFecha.configure(text=f"{self.fecha_seleccionada}")
        print(f"Fecha seleccionada: {self.fecha_seleccionada}")

        # Cerrar la ventana emergente
        self.ventana_calendario.destroy()


class entradaLista(CTkFrame):
    def __init__(self, parent, text1, text2, text3, text4, text5):
        super().__init__(parent, fg_color="white", corner_radius=16)

        # Configurar proporción uniforme para columnas y filas
        self.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="col")
        self.rowconfigure(0, weight=1, uniform="row")

        # Crear los elementos de texto
        nombreCargo = tinyText(self, text1)
        nombreCargo.configure(anchor="center")
        nombreEscuela = tinyText(self, text2)
        nombreEscuela.configure(anchor="center")
        modalidadConcurso = tinyText(self, text3)
        modalidadConcurso.configure(anchor="center")
        fechaInicio = tinyText(self, text4)
        fechaInicio.configure(anchor="center")
        fechaFin = tinyText(self, text5)
        fechaFin.configure(anchor="center")

        # Ubicar elementos en la grilla con espaciado uniforme
        nombreCargo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        nombreEscuela.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        modalidadConcurso.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        fechaInicio.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)
        fechaFin.grid(row=0, column=4, sticky="nsew", padx=5, pady=5)


class formularioSimple(CTkFrame):
    def __init__(self, parent, titulo):
        super().__init__(parent, fg_color="transparent", corner_radius=16)

        self.tituloLab = mediumText(self, titulo)
        self.tituloLab.pack(anchor = "nw")

        self.entradaTexto = CTkEntry(self, width = 500, height = 50, corner_radius= 16, border_width=0, fg_color= "white", font = (("Labrada", 20)), justify = "left")
        self.entradaTexto.pack(anchor = "nw", pady = 20)



class CollapsiblePanel(CTkFrame):
    def __init__(self, parent, title, *args, **kwargs):
        super().__init__(parent, fg_color= "#DEEDFD", *args, **kwargs)

        #Vista colapsada

        vistaColapsadaFrame = CTkFrame(self, fg_color= "transparent")
        vistaColapsadaFrame.pack(fill="x", padx=5, pady=5, expand=True)

        self.titulo = smallText(vistaColapsadaFrame, title)
        self.titulo.pack(side = "left", padx = 20)
        
        # Botón para expandir/colapsar el contenido
        self.toggle_button = iconoClickable(vistaColapsadaFrame, "ExpandIcon", 35, 35, self.toggle)
        self.toggle_button.pack(side="right", padx=20)
        
        # Frame interno que contiene el contenido del panel
        self.content_frame = CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="x", padx=5, pady=5)

        
        
        # Iniciar colapsado
        self._is_collapsed = True
        self.content_frame.pack_forget()

    def toggle(self):
        """Expandir o colapsar el contenido del panel."""
        if self._is_collapsed:
            self.content_frame.pack(fill="x", padx=5, pady=5)
        else:
            self.content_frame.pack_forget()
        self._is_collapsed = not self._is_collapsed


class tituloSubtituloSimple(CTkFrame):
    def __init__(self, parent, titulo, subtitulo):
        super().__init__(parent, fg_color="transparent", corner_radius=16)

        tituloLab = mediumText(self, titulo)
        tituloLab.pack(anchor = "nw")

        entradaTexto = tinyText(self, subtitulo)
        entradaTexto.pack(anchor = "nw",padx = 30, pady = 20)



import re
from tkinter import StringVar

"""class preguntaCuestionario(CTkFrame):
    def __init__(self, parent, titulo):
        super().__init__(parent, fg_color="transparent", corner_radius=16)

        # Label con el título
        tituloLab = smallText(self, titulo)
        tituloLab.configure(wraplength=520, justify="left")
        tituloLab.pack(side="left", padx=30)

        # Variable para controlar el contenido del Entry
        self.valor_var = StringVar()
        self.valor_var.trace("w", self.validar_entrada)  # Llamada a la función de validación en cada cambio

        # Campo de entrada con la variable asignada
        self.entradaTexto = CTkEntry(self, textvariable=self.valor_var, width=180, height=40, corner_radius=16, 
                                      border_width=0, fg_color="white", font=("Labrada", 20), justify="center")
        self.entradaTexto.pack(side="right", padx=100)

    def validar_entrada(self, *args):
        # Obtener el contenido del StringVar
        valor = self.valor_var.get()

        # Expresión regular para valores entre 0.00 y 5.00 con 2 decimales
        if re.fullmatch(r"^0(\.\d{0,2})?$|^[1-4](\.\d{0,2})?$|^5(\.00?)?$", valor):
            pass  # El valor es válido, no se hace nada
        else:
            self.valor_var.set(valor[:-1])  # Elimina el último carácter inválido"""





class preguntaCuestionario(CTkFrame):
    def __init__(self, parent, titulo, modo=1):
        super().__init__(parent, fg_color="transparent", corner_radius=16)

        self.modo = modo  # Atributo para definir el modo de validación

        # Label con el título
        tituloLab = smallText(self, titulo)
        tituloLab.configure(wraplength=520, justify="left")
        tituloLab.pack(side="left", padx=30)

        # Variable para controlar el contenido del Entry
        self.valor_var = StringVar()
        self.valor_var.trace("w", self.validar_entrada)  # Llamada a la función de validación en cada cambio

        # Campo de entrada con la variable asignada
        self.entradaTexto = CTkEntry(self, textvariable=self.valor_var, width=180, height=40, corner_radius=16, 
                                      border_width=0, fg_color="white", font=("Labrada", 20), justify="center")
        self.entradaTexto.pack(side="right", padx=100)


    def validar_entrada(self, *args):
        # Obtener el contenido del StringVar
        valor = self.valor_var.get()

        if self.modo == 1:
            # Modo 1: Valores entre 0.00 y 1.00 con 2 decimales
            if re.fullmatch(r"^0(\.\d{0,2})?$|^1(\.00?)?$", valor):
                pass  # El valor es válido, no se hace nada
            else:
                self.valor_var.set(valor[:-1])  # Elimina el último carácter inválido

        elif self.modo == 2:
            # Modo 2: Valores enteros entre 0 y 100
            if re.fullmatch(r"^[0-9]{1,2}$|^100$", valor):
                pass  # El valor es válido, no se hace nada
            else:
                self.valor_var.set(valor[:-1])  # Elimina el último carácter inválido"""        

        elif self.modo == 3:
            # Modo 3: Valores entre 0.00 y 5.0 con 2 decimales
            if re.fullmatch(r"^0(\.\d{0,2})?$|^[1-4](\.\d{0,2})?$|^5(\.0?)?$", valor):
                pass  # El valor es válido, no se hace nada
            else:
                self.valor_var.set(valor[:-1])  # Elimina el último carácter inválido

        elif self.modo == 4:
            # Modo 4: Número entero entre 0 y 10
            if re.fullmatch(r"^[0-9]$|^10$", valor):
                pass
            else:
                self.valor_var.set(valor[:-1])

        elif self.modo == 5:
            # Modo 5: Número entero entre 0 y 20
            if re.fullmatch(r"^[0-9]$|^[1][0-9]$|^20$", valor):
                pass
            else:
                self.valor_var.set(valor[:-1])

        elif self.modo == 6:
            # Modo 6: Número entero entre 0 y 40
            if re.fullmatch(r"^[0-9]$|^[1-3][0-9]$|^40$", valor):
                pass
            else:
                self.valor_var.set(valor[:-1])

        elif self.modo == 7:
            # Modo 7: Número entero entre 0 y 60
            if re.fullmatch(r"^[0-9]$|^[1-5][0-9]$|^60$", valor):
                pass
            else:
                self.valor_var.set(valor[:-1])


