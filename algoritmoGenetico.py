import math

# coincideraciones 
# 1px = 1m
#

class AlgGeneticoParacaidas:
    def __init__(self, initial_altitude):
        self.chromosomes = []

        self.initial_altitude = initial_altitude
        self.g = 9.81
        self.weight = 80
        self.parachute_area = 10  # Un paracaídas desafiante
        self.coeficiente_arrastre = 1.0
        self.air_d = 1.225
        self.initial_speed = 0
        self.dt = 0.1
        self.safe_landing_speed = 5.5 # Metros por segundo m/s

        self.generation = 0;

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

        

obj = AlgGeneticoParacaidas(initial_altitude=20)
print(obj.simulate_fall())

