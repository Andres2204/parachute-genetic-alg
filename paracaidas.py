import tkinter as tk
import math
from PIL import Image, ImageTk

class Paracaidas:
    def __init__(self, root):
        self.root = root
        self.root.title("Paracaidas")
        self.root.geometry("600x600")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)

        # Parámetros físicos
        self.initial_altitude = 300
        self.g = 9.81
        self.weight = 80
        self.parachute_area = 10  # Un paracaídas desafiante
        self.coeficiente_arrastre = 1.0
        self.air_d = 1.225
        self.initial_speed = 0
        self.dt = 0.1
        self.safe_landing_speed = 5.5 # Metros por segundo m/s
        self.y = 10

        # Centrar la ventana
        self.centrar_ventana()
        
        # Crear la interfaz
        self.crear_interfaz()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = 600
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def crear_interfaz(self):
        # Titulo
        titulo = tk.Label(
            self.root,
            text="Paracaidas",
            bg='#f0f0f0', 
            fg='#2c3e50'
        )
        titulo.pack(pady=20)

        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(padx=30, fill='both', expand=True)

        # Hornet volando
        self.crear_canvas(main_frame, "planeando.png", "parado.png", "estampado.png")

        # datos
        self.y_label = tk.Label(
            main_frame,
            text=f"y {self.y}",
            bg='#f0f0f0', 
            fg='#2c3e50'
        )
        self.y_label.grid(row=2, column=0, pady=5)
        
        # boton de iniciar / reiniciar 
        self.start_button = tk.Button(
            main_frame,
            text='Iniciar',
            command=self.start_simulation,
        )
        self.start_button.grid(row=2, column=1)
    
    def crear_canvas(self, parent, sprite_planeando, sprint_parado, sprite_estampado):
        self.canvas = tk.Canvas(
            parent,
            width=590,
            height=400,
            bg='white'
        )
        self.canvas.grid(row=1, column=0, columnspan=2)

        img = Image.open(sprite_planeando)
        self.sprite_height = 150
        img = img.resize((100, self.sprite_height))  # ancho=150px, alto=150px
        self.photo = ImageTk.PhotoImage(img)
        self.sprite = self.canvas.create_image(230, self.y, image=self.photo, anchor='nw')

        self.ground_y_coord = 350
        self.ground = self.canvas.create_line(0, self.ground_y_coord, 590, self.ground_y_coord, width=5, fill='green')
        self.canvas.create_rectangle(0, self.ground_y_coord, 590, 600, fill='brown', outline='green')

    def start_simulation(self):
        self.speed = self.initial_speed
        self.canvas.coords(self.sprite, 230, 10)
        self.simulation = True
        self.simulation_step()

    def simulation_step(self):
        if not self.simulation:
            # get new gen
            pass
        # Actualizar velocidad y posición
        fuerza_gravedad = self.weight * self.g
        magnitud_arrastre = 0.5 * self.air_d * (self.speed*2) * self.coeficiente_arrastre * self.parachute_area 
        fuerza_neta = fuerza_gravedad - math.copysign(1.0, self.speed) * magnitud_arrastre
        aceleracion = fuerza_neta / self.weight
        self.speed += aceleracion * self.dt
        self.y += self.speed*self.dt
        self.canvas.coords(self.sprite, 230, self.y)
        self.update_labels()

        if self.y < self.ground_y_coord - self.sprite_height:
            self.root.after(50, self.simulation_step)
        else:
            self.simulation = False

    def update_labels(self):
        self.y_label.config(text=f"y: {self.y}")

root = tk.Tk()
app = Paracaidas(root)
root.mainloop()
