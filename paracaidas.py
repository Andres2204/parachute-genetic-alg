import tkinter as tk
from PIL import Image, ImageTk

class Paracaidas:
    def __init__(self, root):
        self.root = root
        self.root.title("Paracaidas")
        self.root.geometry("600x600")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)

        # Parámetros físicos
        self.g = 0.5         # gravedad "virtual"
        self.r = 0.3         # resistencia / planeabilidad
        self.vy = 0          # velocidad vertical
        self.y = 50          # posición inicial en Y
        
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
        
        self.r_label = tk.Label(
            main_frame,
            text=f"r {self.r}",
            bg='#f0f0f0', 
            fg='#2c3e50'
        )
        self.r_label.grid(row=3, column=0, pady=5)
        
        # boton de iniciar / reiniciar 
        self.start_button = tk.Button(
            main_frame,
            text='Iniciar',
            command=self.update,
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
        self.sprite_height = 100
        img = img.resize((100, self.sprite_height))  # ancho=150px, alto=150px
        self.photo = ImageTk.PhotoImage(img)
        self.sprite = self.canvas.create_image(230, 10, image=self.photo, anchor='nw')

        self.ground_y_coord = 350
        self.ground = self.canvas.create_line(0, self.ground_y_coord, 590, self.ground_y_coord, width=5, fill='green')
        self.canvas.create_rectangle(0, self.ground_y_coord, 590, 600, fill='brown', outline='green')

    def update(self):
        # Actualizar velocidad y posición
        self.vy += self.g - self.r   # velocidad con gravedad y resistencia
        self.y += self.vy

        # Mover sprite
        self.canvas.coords(self.sprite, 230, self.y)
        print(self.canvas.coords(self.sprite))
        self.update_labels()
        
        # Detener en el suelo
        if self.y + self.sprite_height < self.ground_y_coord:
            self.root.after(50, self.update)  # sigue cayendo
        else:
            print("¡Aterrizó!")

    def update_labels(self):
        self.y_label.config(text=f"y: {self.y}")
        self.r_label.config(text=f"r: {self.r}")


root = tk.Tk()
app = Paracaidas(root)
root.mainloop()
