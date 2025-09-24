import tkinter as tk
from PIL import Image, ImageTk
import random
from algoritmoGenetico import AlgGeneticoParacaidas

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
        self.simulation = False

        # Centrar la ventana
        self.centrar_ventana()
        
        # Crear la interfaz
        self.crear_interfaz()
        # Estado del algoritmo genético en UI
        self.ga = None
        self.best_chromosome = None
        self.generations_to_run = 0
        self.is_evolving = False
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = 800
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def crear_interfaz(self):
        # Titulo
        titulo = tk.Label(
            self.root,
            text="Paracaidista - Simulación",
            bg='#f0f0f0', 
            fg='#2c3e50',
            font=('Arial', 16, 'bold')
        )
        titulo.pack(pady=10)

        # Frame principal con dos columnas
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Columna izquierda - Simulación
        left_frame = tk.Frame(main_frame, bg="white", relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # Canvas de simulación
        self.crear_canvas(left_frame, "planeando.png", "parado.png", "estampado.png")

        # Botones de control
        button_frame = tk.Frame(left_frame, bg="white")
        button_frame.pack(pady=10)
        
        self.setup_button = tk.Button(
            button_frame,
            text='Setup',
            command=self.setup_random,
            bg='#3498db',
            fg='white',
            font=('Arial', 12),
            width=10
        )
        self.setup_button.pack(side='left', padx=5)
        
        self.start_button = tk.Button(
            button_frame,
            text='Start',
            command=self.handle_start,
            bg='#27ae60',
            fg='white',
            font=('Arial', 12),
            width=10
        )
        self.start_button.pack(side='left', padx=5)

        # Columna derecha - Panel de información
        right_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='raised', bd=2)
        right_frame.pack(side='right', fill='y', padx=(5, 0))
        right_frame.config(width=150)
        right_frame.pack_propagate(False) # Evita que el frame se encoja

        # Panel de información
        panel_label = tk.Label(
            right_frame,
            text="Panel",
            bg='#ecf0f1',
            fg='#2c3e50',
            font=('Arial', 14, 'bold')
        )
        panel_label.pack(pady=10)

        # Información de la generación
        self.generation_label = tk.Label(
            right_frame,
            text="Generación: 0",
            bg='#ecf0f1',
            fg='#2c3e50',
            font=('Arial', 12)
        )
        self.generation_label.pack(pady=5, anchor='w', padx=10)

        # Información de parámetros
        self.velocity_label = tk.Label(
            right_frame,
            text="V: 0.00 m/s",
            bg='#ecf0f1',
            fg='#2c3e50',
            font=('Arial', 11)
        )
        self.velocity_label.pack(pady=2, anchor='w', padx=10)

        self.area_label = tk.Label(
            right_frame,
            text=f"A: {self.parachute_area:.2f} m²",
            bg='#ecf0f1',
            fg='#2c3e50',
            font=('Arial', 11)
        )
        self.area_label.pack(pady=2, anchor='w', padx=10)

        self.drag_label = tk.Label(
            right_frame,
            text=f"B: {self.coeficiente_arrastre:.2f}",
            bg='#ecf0f1',
            fg='#2c3e50',
            font=('Arial', 11)
        )
        self.drag_label.pack(pady=2, anchor='w', padx=10)

        self.weight_label = tk.Label(
            right_frame,
            text=f"P: {self.weight:.2f} kg",
            bg='#ecf0f1',
            fg='#2c3e50',
            font=('Arial', 11)
        )
        self.weight_label.pack(pady=2, anchor='w', padx=10)

        # Fitness
        self.fitness_label = tk.Label(
            right_frame,
            text="Fitness: 0.00",
            bg='#ecf0f1',
            fg='#e74c3c',
            font=('Arial', 12, 'bold')
        )
        self.fitness_label.pack(pady=10, anchor='w', padx=10)
        
        # Etiqueta de estado
        self.status_label = tk.Label(
            right_frame,
            text="Estado: listo",
            bg='#ecf0f1',
            fg='#7f8c8d',
            font=('Arial', 10)
        )
        self.status_label.pack(pady=5, anchor='w', padx=10)
    
    def crear_canvas(self, parent, sprite_planeando, sprite_parado, sprite_estampado):
        self.canvas = tk.Canvas(
            parent,
            width=600, # Ajustado al espacio
            height=400,
            bg='lightblue'
        )
        self.canvas.pack(pady=10, padx=10)

        # Guardar referencias a los nombres de archivo de las imágenes
        self.sprite_planeando_path = sprite_planeando
        self.sprite_parado_path = sprite_parado
        self.sprite_estampado_path = sprite_estampado
        
        # Cargar sprite inicial (planeando)
        self.load_sprite(self.sprite_planeando_path)
        
        # Suelo
        self.ground_y_coord = 350
        self.ground = self.canvas.create_line(0, self.ground_y_coord, 600, self.ground_y_coord, width=5, fill='green')
        self.canvas.create_rectangle(0, self.ground_y_coord, 600, 400, fill='brown', outline='green')

    # ## MÉTODO NUEVO ##
    def load_sprite(self, image_path):
        """Carga una imagen, la muestra en el canvas y guarda su referencia."""
        try:
            image = Image.open(image_path)
            self.sprite_height = 100
            image = image.resize((100, self.sprite_height))
            self.photo_image = ImageTk.PhotoImage(image)


            # Si el sprite ya existe, lo actualizamos. Si no, lo creamos.
            if hasattr(self, 'sprite'):
                self.canvas.itemconfig(self.sprite, image=self.photo_image)
            else:
                self.sprite = self.canvas.create_image(
                    150, 10,  # Coordenadas x, y centradas
                    anchor='n',  # Anclar en el centro superior
                    image=self.photo_image
                )
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de imagen '{image_path}'.")
            self.sprite = self.canvas.create_rectangle(150, 10, 200, 60, fill="red")
            self.sprite_height = 50

    def start_simulation(self):
        if self.simulation: # No hacer nada si ya está corriendo
            return
        self.speed = self.initial_speed
        self.y = 10
        # Cargar el sprite de planeo y moverlo a la posición inicial
        self.load_sprite(self.sprite_planeando_path)
        self.canvas.coords(self.sprite, 150, self.y)
        
        self.simulation = True
        self.simulation_step()

    def setup_random(self):
        """Inicializa valores aleatorios según los atributos y actualiza el panel."""
        # Si hay evolución/animación en curso, no permitir cambios
        if self.simulation or self.is_evolving:
            return

        # Rango razonable para atributos ajustables
        self.parachute_area = random.uniform(10, 40)
        self.coeficiente_arrastre = random.uniform(1.0, 2.5)
        self.weight = random.uniform(60, 100)

        # Reiniciar etiquetas y estado
        self.speed = 0.0
        self.y = 10
        self.best_chromosome = None
        self.fitness_label.config(text="Fitness: 0.00")
        self.generation_label.config(text="Generación: 0")
        self.status_label.config(text="Estado: setup aleatorio")
        self.update_labels()
        # Reset visual
        self.load_sprite(self.sprite_planeando_path)
        self.canvas.coords(self.sprite, 150, self.y)

    def handle_start(self):
        """Ejecuta GA por N generaciones y luego anima caída con el mejor cromosoma."""
        if self.simulation or self.is_evolving:
            return

        # Parámetros GA (pueden exponerse en UI si se desea)
        time_limit = 60
        population_size = 8
        self.ga = AlgGeneticoParacaidas(
            initial_altitude=self.initial_altitude,
            safe_landing_speed=self.safe_landing_speed,
            time_limit=time_limit,
            population_size=population_size
        )

        self.generations_to_run = 60
        self.is_evolving = True
        self.status_label.config(text="Estado: evolucionando...")
        self.run_evolution_step()

    def run_evolution_step(self):
        if not self.is_evolving or self.ga is None:
            return
        if self.generations_to_run <= 0:
            # terminar evolución, usar mejor cromosoma actual
            best = max(self.ga.chromosomes, key=lambda c: c.fitness)
            self.best_chromosome = best
            self.parachute_area = best.area
            self.coeficiente_arrastre = best.coe
            self.fitness_label.config(text=f"Fitness: {best.fitness:.2f}")
            self.status_label.config(text="Estado: animando caída")
            self.is_evolving = False
            # iniciar animación con parámetros optimizados
            self.start_simulation()
            return

        # Una generación
        gen, best = self.ga.get_next_gen()
        self.generation_label.config(text=f"Generación: {gen}")
        self.fitness_label.config(text=f"Fitness: {best.fitness:.2f}")
        # Mostrar valores del mejor en panel
        self.parachute_area = best.area
        self.coeficiente_arrastre = best.coe
        self.update_labels()

        self.generations_to_run -= 1
        # Programar siguiente paso sin bloquear UI
        self.root.after(30, self.run_evolution_step)

    def simulation_step(self):
        if not self.simulation:
            return

        # Actualizar velocidad y posición
        fuerza_gravedad = self.weight * self.g
        # ## CORRECCIÓN FÍSICA AQUÍ ##
        magnitud_arrastre = 0.5 * self.air_d * (self.speed**2) * self.coeficiente_arrastre * self.parachute_area 
        fuerza_neta = fuerza_gravedad - magnitud_arrastre
        aceleracion = fuerza_neta / self.weight
        self.speed += aceleracion * self.dt
        self.y += self.speed * self.dt # La y aumenta hacia abajo
        
        self.canvas.coords(self.sprite, 150, self.y)
        self.update_labels()

        if self.y < self.ground_y_coord - self.sprite_height:
            self.root.after(30, self.simulation_step) # 30 ms para una animación más fluida
        else:
            self.simulation = False
            # ## MEJORA DE ATERRIZAJE AQUÍ ##
            if self.speed <= self.safe_landing_speed:
                # Aterrizaje seguro
                self.load_sprite(self.sprite_parado_path)
            else:
                # Aterrizaje fallido
                self.load_sprite(self.sprite_estampado_path)
            
            # Colocar el sprite justo en el suelo
            self.canvas.coords(self.sprite, 150, self.ground_y_coord - self.sprite_height)
            self.update_labels() # Actualizar una última vez con la velocidad final

    # ## MÉTODO CORREGIDO ##
    def update_labels(self):
        """Actualiza las etiquetas del panel de información."""
        self.velocity_label.config(text=f"V: {self.speed:.2f} m/s")
        self.area_label.config(text=f"A: {self.parachute_area:.2f} m²")
        self.drag_label.config(text=f"B: {self.coeficiente_arrastre:.2f}")
        self.weight_label.config(text=f"P: {self.weight:.2f} kg")

if __name__ == "__main__":
    root = tk.Tk()
    app = Paracaidas(root)
    root.mainloop()