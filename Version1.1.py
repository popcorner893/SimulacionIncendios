import customtkinter as ctk
import simulacionFuego



# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("dark")  # Modo oscuro
ctk.set_default_color_theme("blue")  # Tema de color por defecto

# Crear la ventana principal
ventanaPrincipal = ctk.CTk()
ventanaPrincipal.title("Grilla de 20x20 Botones")
ventanaPrincipal.geometry("400x400")  # Tamaño inicial de la ventana

boton1 = ctk.CTkButton(
    ventanaPrincipal,
    text = "Inicializar Juego",
    ANCHO = 40,
    ALTO = 20,
    corner_radius= 2,
    fg_color= "blue",
    command = lambda: simulacionFuego.ejecutarSimulacion.iniciar_juego()
)

boton1.grid(fila = 0, column = 0, padx = 20, pady = 20, sticky = "ew")


# Iniciar el bucle principal
ventanaPrincipal.mainloop()




