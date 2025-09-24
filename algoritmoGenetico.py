import math
from types import SimpleNamespace 
import random


# coincideraciones 
# 1px = 1m
#
# chromosome = [tiempo, parachute_area, coeficiente_arrastre]
# fitness 
#


class AlgGeneticoParacaidas:
    def __init__(self, initial_altitude, safe_landing_speed, time_limit, population_size):
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
        self.time_limit = time_limit

        self.generate_population()

    def generate_population(self):
       
        self.chromosomes = []
        for _ in range(self.population_size):         
            random_area = random.uniform(10, 40)
            random_coe = random.uniform(1, 2.5)
            chromosome = create_chromosome(random_area, random_coe)
            chromosome.fitness = self.fitness(chromosome) # Calcula el fitness inicial
            self.chromosomes.append(chromosome)
    
    # selection 
    def select_chromosomes(self):

        def _tournament(k=3):
            competitors = random.sample(self.chromosomes, k)
            winner = max(competitors, key=lambda c: c.fitness)
            return winner

        parent1 = _tournament()
        parent2 = _tournament()
        
        while parent1 is parent2:
            parent2 = _tournament()
            
        return parent1, parent2

    # mixing and mutation 
    def mixing(self, c1, c2):

        child_area = (c1.area + c2.area) / 2.0
        child_coe = (c1.coe + c2.coe) / 2.0
        
        # El nuevo cromosoma ya se crea con su fitness evaluado.
        return self._create_chromosome(child_area, child_coe)

    def mutate(self, chromosome):

        mutated = False
        if random.random() < self.mutation_rate:
            change_factor = 1 + random.uniform(-self.mutation_strength, self.mutation_strength)
            chromosome.area *= change_factor
            chromosome.area = max(10, min(40, chromosome.area))
            mutated = True

        if random.random() < self.mutation_rate:
            change_factor = 1 + random.uniform(-self.mutation_strength, self.mutation_strength)
            chromosome.coe *= change_factor
            chromosome.coe = max(1, min(2.5, chromosome.coe))
            mutated = True

        if mutated:
            chromosome.fitness = self.fitness(chromosome)
            
        return chromosome

    # fitness 
    def fitness(self, chromosome):
        final_speed, total_time = self.simulate_fall(chromosome.area, chromosome.coe)

        # Penalización velocidad
        if final_speed <= self.safe_landing_speed:
            score_vel = 1.0
        else:
            score_vel = self.safe_landing_speed / final_speed
        
        score_time = max(0, 1 - (total_time / self.time_limit))

        # Fitness combinado
        fitness = score_vel * score_time
        return fitness

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

        nueva_poblacion = []

        # --- ELITISMO ---
        elite_chromosomes = sorted(self.chromosomes, key=lambda x: x.fitness, reverse=True)[:2]
        nueva_poblacion.extend(elite_chromosomes)

        # --- REPRODUCCIÓN ---
        while len(nueva_poblacion) < len(self.chromosomes):
            # Seleccionar padres
            c1, c2 = self.select_chromosomes()

            # Cruzarlos
            child = self.mixing(c1, c2)

            # Mutar hijo
            self.mutate(child)

            # Evaluar fitness
            child.fitness = self.fitness(child)

            # Agregar a nueva población
            nueva_poblacion.append(child)

        # Actualizar la población
        self.chromosomes = nueva_poblacion

        # Obtener mejor cromosoma de esta generación
        best_chromosome = max(self.chromosomes, key=lambda x: x.fitness)

        self.generation += 1
        return self.generation, best_chromosome
        """
        # selecionar mansitos
        c1, c2 = self.select_chromosomes()

        # cruzarlos
        child = self.mixing(c1, c2)

        # mutar el hijo
        mutate(child)

        # comparar hijo
        child.fitness = self.fitness(child);

        # elitismo
        elite_chromosomes = sorted(self.chromosomes, key=lambda x: x.fitness, reverse=True)[:2]
        
        # nueva poblacion
        
        # mandar mejor cromosoma 

        best_chromosome = ...
        self.generation += 1
        return self.generation, best_chromosome
        """
        

def create_chromosome(parachute_area, coeficiente_arrastre):
    
    return SimpleNamespace(
        area=parachute_area,
        coe=coeficiente_arrastre,
        fitness=0
    )

obj = AlgGeneticoParacaidas(initial_altitude=240, safe_landing_speed=5.5, time_limit=60, population_size=5)
velocidad_final, tiempo_total = obj.simulate_fall(20, 2)  # área = 10 m²
fitness = obj.fitness(create_chromosome(20, 2))
print(f"Velocidad de impacto: {velocidad_final:.2f} m/s")
print(f"Tiempo de caída: {tiempo_total:.2f} s")
print(f"Fitness: {fitness:.2f}")



