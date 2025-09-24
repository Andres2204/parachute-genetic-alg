import math

# coincideraciones 
# 1px = 1m
#

class AlgGeneticoParacaidas:
    def __init__(self, initial_altitude, safe_landing_speed, population_size):
        self.chromosomes = []
        self.generation = 0
        self.population_size = population_size

        self.initial_altitude = initial_altitude
        self.g = 9.81
        self.weight = 80
        self.parachute_area = 10
        self.coeficiente_arrastre = 1.0
        self.air_d = 1.225
        self.initial_speed = 0
        self.dt = 0.1
        self.safe_landing_speed = safe_landing_speed # Metros por segundo m/s

        self.generate_population()

    def generate_population(self):
        pass
    
    # selection 

    # mixing and mutation 
    def mixing(self, c1, c2):
        pass

    def mutate(self, chromosome):
        pass

    # fitness 
    def fitness(self, chromosome):
        pass

    def simulate_fall(self):
        height = self.initial_altitude
        speed = self.initial_speed
        while altitud > 0:
            area_actual = self.parachute_area
            fuerza_gravedad = self.weight * self.g
            magnitud_arrastre = 0.5 * self.air_d * (speed**2) * self.coeficiente_arrastre * area_actual 
            fuerza_neta = fuerza_gravedad - math.copysign(1.0, speed) * magnitud_arrastre
            aceleracion = fuerza_neta / self.weight
            speed += aceleracion * self.dt
            height -= speed * self.dt
        
        # Clamp para evitar overshoot
        if height < 0:
            height = 0
        return abs(speed)  # Abs para seguridad

    def get_next_gen(self):
        # general program flow


        self.generation += 1
        return self.generation, best_chromosome
        

obj = AlgGeneticoParacaidas(initial_altitude=20, safe_landing_speed=5.5)
print(obj.simulate_fall())

