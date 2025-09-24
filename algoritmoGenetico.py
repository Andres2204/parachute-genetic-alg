import math

# coincideraciones 
# 1px = 1m
#
# chromosome = [tiempo, parachute_area, coeficiente_arrastre]
#
#

class AlgGeneticoParacaidas:
    def __init__(self, initial_altitude, safe_landing_speed, population_size):
        self.chromosomes = []
        self.generation = 0
        self.population_size = population_size

        self.initial_altitude = initial_altitude
        self.g = 9.81
        self.weight = 80
        self.air_d = 1.225
        self.initial_speed = 0
        self.dt = 0.1
        self.safe_landing_speed = safe_landing_speed # Metros por segundo m/s

        self.generate_population()

    def generate_population(self):
        pass
    
    # selection 
    def select_chromosomes(self, population):
        c1, c2 = 1,2 
        return c1, c2

    # mixing and mutation 
    def mixing(self, c1, c2):
        pass

    def mutate(self, chromosome):
        pass

    # fitness 
    def fitness(self, chromosome):
        pass

    def simulate_fall(self, parachute_area, coeficiente_arrastre):
        height = self.initial_altitude
        speed = self.initial_speed
        time = 0.0
        while height > 0:
            fuerza_gravedad = self.weight * self.g
            magnitud_arrastre = 0.5 * self.air_d * (speed**2) * coeficiente_arrastre * parachute_area 
            fuerza_neta = fuerza_gravedad - math.copysign(1.0, speed) * magnitud_arrastre
            aceleracion = fuerza_neta / self.weight
            speed += aceleracion * self.dt
            height -= speed * self.dt
            time += self.dt
        
        # Clamp para evitar overshoot
        if height < 0:
            height = 0
        return abs(speed), time  # Abs para seguridad

    def get_next_gen(self):
        # general program flow

        best_chromosome = 1
        self.generation += 1
        return self.generation, best_chromosome
        

obj = AlgGeneticoParacaidas(initial_altitude=240, safe_landing_speed=5.5, population_size=5)
velocidad_final, tiempo_total = obj.simulate_fall(20, 2)  # área = 10 m²
print(f"Velocidad de impacto: {velocidad_final:.2f} m/s")
print(f"Tiempo de caída: {tiempo_total:.2f} s")


