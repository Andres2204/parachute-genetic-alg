import math
from types import SimpleNamespace 
import random

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
        self.mutation_rate = 1
        self.mutation_strength = 0.9

        self.min_area = 15
        self.max_area = 35
        
        self.min_coe = 1.0
        self.max_coe = 2.5
        

        self.generate_population()

    def generate_population(self):
       
        self.chromosomes = []
        for _ in range(self.population_size):         
            random_area = random.uniform(self.min_area, self.max_area-15)
            random_coe = random.uniform(self.min_coe, self.max_coe-1)
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
        #print("---Mutating chromosome:", chromosome)
        # ESTRATEGIA 1: Mutación Gaussiana
        if random.random() < self.mutation_rate:
            gaussian_change = random.gauss(0, 0.1 * chromosome.area)  # Menor desviación
            chromosome.area += gaussian_change
            chromosome.area = max(self.min_area, min(self.max_area, chromosome.area))
            mutated = True
    
        if random.random() < self.mutation_rate:
            gaussian_change = random.gauss(0, 0.1 * chromosome.coe)  # Menor desviación
            chromosome.coe += gaussian_change
            chromosome.coe = max(self.min_coe, min(self.max_coe, chromosome.coe))  # Límites correctos
            mutated = True
    
        # ESTRATEGIA 2: Mutación forzada ocasional
        if random.random() < 0.05:  # Independiente de mutated
            if random.random() < 0.5:
                chromosome.area *= random.uniform(0.7, 1.3)
                chromosome.area = max(self.min_area, min(self.max_area, chromosome.area))
            else:
                chromosome.coe *= random.uniform(0.7, 1.3)
                chromosome.coe = max(self.min_coe, min(self.max_coe, chromosome.coe))
            mutated = True
        #print("---Resulting chromosome:", chromosome)
        return chromosome, mutated
    
    def fitness(self, chromosome, t_max=60.0):
        final_speed, time = self.simulate_fall(chromosome.area, chromosome.coe)
        score_vel = self.safe_landing_speed / final_speed  # Siempre, sin cap en 1.0 para recompensar v más bajas
    
        if time > self.time_limit:
            target_time = 0.6 * t_max
            sigma = 0.4 * t_max
        else:
            target_time = 0.8 * t_max
            sigma = 0.2 * t_max

        score_time = math.exp(-((time - target_time) ** 2) / (2 * sigma ** 2))
    
        fitness = 0.7 * score_vel + 0.3 * score_time
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
        
        if height < 0:
            height = 0
        return abs(speed), time

    def get_next_gen(self):
        chromosomes = sorted(self.chromosomes, key=lambda x: x.fitness, reverse=True)
        new_population = chromosomes[:2]
        
        for _ in range(3):
            c1, c2 = self.select_chromosomes()
            child = self.mixing(c1, c2)
            child, _ = self.mutate(child)
            child.fitness = self.fitness(child)
            new_population.append(child)
            print("[gc] ", child)
        
        new_population.extend(chromosomes[2:self.population_size - len(new_population) + 2])
        self.chromosomes = sorted(new_population[:self.population_size], key=lambda x: x.fitness, reverse=True)
        
        best_chromosome = self.chromosomes[0]
        self.generation += 1
        return self.generation, best_chromosome

def create_chromosome(parachute_area, coeficiente_arrastre):
    return SimpleNamespace(
        area=parachute_area,
        coe=coeficiente_arrastre,
        fitness=0
    )

obj = AlgGeneticoParacaidas(initial_altitude=240, safe_landing_speed=5.5, time_limit=60, population_size=50)
for _ in range(0, 300):
    gen, chromosome = obj.get_next_gen();
    speed, time = obj.simulate_fall(chromosome.area, chromosome.coe)
    print("[Best] ", chromosome, gen)
    print(f"Velocidad de impacto: {speed:.2f} m/s")
    print(f"Tiempo de caída: {time:.2f} s")
    print(f"Fitness: {chromosome.fitness:.2f}", end='\n\n')
