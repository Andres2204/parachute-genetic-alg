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
        self.mutation_rate = 0.3
        self.mutation_strength = 0.5

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
        """
        Selección por ruleta ponderada (roulette wheel selection)
        Más eficiente y diversa que el torneo simple
        """
        # Calcular fitness total y crear lista de probabilidades acumulativas
        total_fitness = sum(c.fitness for c in self.chromosomes)
        
        # Evitar división por cero
        if total_fitness == 0:
            # Si todos tienen fitness 0, selección aleatoria
            parent1 = random.choice(self.chromosomes)
            parent2 = random.choice([c for c in self.chromosomes if c != parent1])
            return parent1, parent2
        
        # Crear lista de probabilidades acumulativas
        cumulative_probs = []
        cumulative_sum = 0
        for chromosome in self.chromosomes:
            cumulative_sum += chromosome.fitness / total_fitness
            cumulative_probs.append(cumulative_sum)
        
        def _roulette_selection():
            r = random.random()
            for i, prob in enumerate(cumulative_probs):
                if r <= prob:
                    return self.chromosomes[i]
            return self.chromosomes[-1]  # Fallback
        
        # Seleccionar dos padres diferentes
        parent1 = _roulette_selection()
        parent2 = _roulette_selection()
        
        # Asegurar que sean diferentes
        attempts = 0
        while parent1 is parent2 and attempts < 10:
            parent2 = _roulette_selection()
            attempts += 1
        
        return parent1, parent2

    # mixing and mutation 
    def mixing(self, c1, c2):

        child_area = (c1.area + c2.area) / 2.0
        child_coe = (c1.coe + c2.coe) / 2.0
        
        # El nuevo cromosoma ya se crea con su fitness evaluado.
        return create_chromosome(child_area, child_coe)

    def mutate(self, chromosome):

        mutated = False
        print("----------Mutating chromosome:", chromosome)
        # ESTRATEGIA 1: Mutación Gaussiana (más suave y controlada)
        if random.random() < self.mutation_rate:
            # Mutación gaussiana para el área
            gaussian_change = random.gauss(0, self.mutation_strength * chromosome.area)
            chromosome.area += gaussian_change
            chromosome.area = max(10, min(40, chromosome.area))
            mutated = True

        if random.random() < self.mutation_rate:
            # Mutación gaussiana para el coeficiente
            gaussian_change = random.gauss(0, self.mutation_strength * chromosome.coe)
            chromosome.coe += gaussian_change
            chromosome.coe = max(1, min(2.5, chromosome.coe))
            mutated = True

        # ESTRATEGIA 2: Mutación forzada ocasional (evita estancamiento)
        if not mutated and random.random() < 0.05:  # 5% de mutación forzada
            if random.random() < 0.5:
                # Mutación grande en área
                chromosome.area *= random.uniform(0.7, 1.3)
                chromosome.area = max(10, min(40, chromosome.area))
            else:
                # Mutación grande en coeficiente
                chromosome.coe *= random.uniform(0.7, 1.3)
                chromosome.coe = max(1, min(2.5, chromosome.coe))
            mutated = True
        print("------------Resulting chromosome:", chromosome)
        return chromosome, mutated
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
            # Selección normal
        c1, c2 = self.select_chromosomes()
        child = self.mixing(c1, c2)
        
        # Mutación mejorada
        child, was_mutated = self.mutate(child)  # o mutate_adaptive
        
        # Solo calcular fitness si mutó o es nuevo
        child.fitness = self.fitness(child)
        
        # Resto del código igual...
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
    

