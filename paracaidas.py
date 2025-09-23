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


        # boton de iniciar / reiniciar 
        move = tk.Button(
            main_frame,
            text='Mover abajo',
            command=self.move,
            padx=100,
            pady=20
        )
        move.grid(row=2, column=0, pady=10)
    
    def crear_canvas(self, parent, sprite_planeando, sprint_parado, sprite_estampado):
        self.canvas = tk.Canvas(
            parent,
            width=590,
            height=400,
            bg='white'
        )
        self.canvas.grid(row=1, column=0, sticky='w')
        img = Image.open(sprite_planeando)
        self.sprite_height = 100
        img = img.resize((100, self.sprite_height))  # ancho=150px, alto=150px
        self.photo = ImageTk.PhotoImage(img)

        self.sprite = self.canvas.create_image(250, 10, image=self.photo, anchor='nw')
        self.ground_y_coord = 350
        self.floor = self.canvas.create_line(0, self.ground_y_coord, 590, self.ground_y_coord, width=5, fill='red')
        self.update()

    def update(self):
        # Actualizar velocidad y posición
        self.vy += self.g - self.r   # velocidad con gravedad y resistencia
        self.y += self.vy

        # Mover sprite
        self.canvas.coords(self.sprite, 295, self.y)
        print(self.canvas.coords(self.sprite))

        # Detener en el suelo
        if self.y + self.sprite_height < self.ground_y_coord:
            self.root.after(50, self.update)  # sigue cayendo
        else:
            print("¡Aterrizó!")

    def move(self):
        self.canvas.move(self.sprite, 0, 3)


root = tk.Tk()
app = Paracaidas(root)
root.mainloop()
