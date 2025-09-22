import tkinter as tk
from PIL import Image, ImageTk

class Paracaidas:
    def __init__(self, root):
        self.root = root
        self.root.title("Paracaidas")
        self.root.geometry("600x600")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)

        self.gravity = 9.8
        self.planability = 2
        
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
        main_frame.pack(padx=30, pady=10, fill='both', expand=True)

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
        self.canvas.grid(row=1, column=0, sticky='w', pady=8)
        img = Image.open(sprite_planeando)
        img = img.resize((100, 100))  # ancho=150px, alto=150px
        self.photo = ImageTk.PhotoImage(img)

        self.sprite = self.canvas.create_image(10, 10, image=self.photo, anchor='nw')
        #canvas.create_oval(100, 10, 180, 80, width=2, fill='blue')

    def move(self):
        self.canvas.move(self.sprite, 0, 3)


root = tk.Tk()
app = Paracaidas(root)
root.mainloop()
