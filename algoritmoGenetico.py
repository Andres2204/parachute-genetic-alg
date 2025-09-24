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
        self.mutation_rate = 0.1
        self.mutation_strength = 0.2

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
        return create_chromosome(child_area, child_coe)

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
        # normal flow
        c1, c2 = self.select_chromosomes()
        child = self.mixing(c1, c2)
        child = self.mutate(child)
        child.fitness = self.fitness(child)
    
        # elite selection (best of generation)
        elite_chromosomes = sorted(self.chromosomes, key=lambda x: x.fitness, reverse=True)[:2]
        new_population = elite_chromosomes.copy()
    
        worst_chromosome = min(self.chromosomes, key=lambda x: x.fitness)
        if child.fitness > worst_chromosome.fitness:
            new_population.append(child)
        else:
            new_population.append(worst_chromosome)
    
        chromosomes_left = [c for c in self.chromosomes if c not in elite_chromosomes and c != worst_chromosome]
        new_population.extend(chromosomes_left)
    
        new_population = new_population[:len(self.chromosomes)]
    
        self.chromosomes = new_population
        best_chromosome = max(self.chromosomes, key=lambda x: x.fitness)
    
        self.generation += 1
        return self.generation, best_chromosome

def create_chromosome(parachute_area, coeficiente_arrastre):
    return SimpleNamespace(
        area=parachute_area,
        coe=coeficiente_arrastre,
        fitness=0
    )

obj = AlgGeneticoParacaidas(initial_altitude=240, safe_landing_speed=5.5, time_limit=60, population_size=5)
for _ in range(0, 1000):
    gen, chromosome = obj.get_next_gen();
    speed, time = obj.simulate_fall(chromosome.area, chromosome.coe)
    print(chromosome, gen)
    print(f"Velocidad de impacto: {speed:.2f} m/s")
    print(f"Tiempo de caída: {time:.2f} s")
    print(f"Fitness: {chromosome.fitness:.2f}", end='\n\n')
    


