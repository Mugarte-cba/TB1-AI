# Importando librerias
import random
import copy

class State:
    # Creando un nuevo estado
    def __init__(self, route: [], distance: int = 0):
        self.route = route
        self.distance = distance

    # Creando una copia
    def deepcopy(self):
        return State(copy.deepcopy(self.route), copy.deepcopy(self.distance))

    #Actualizando distancia
    def update_distance(self, matrix, home):

        #Reiniciando distancia
        self.distance = 0
        # Mantenga un registro de salida de la ciudad
        from_index = home
        # Recorre todas las ciudades de la ruta actual
        for i in range(len(self.route)):
            self.distance += matrix[from_index][self.route[i]]
            from_index = self.route[i]
        #Añadir la distancia de vuelta a home
        self.distance += matrix[from_index][home]

class City:
    #Creando una nueva ciudad
    def __init__(self, index: int, distance: int):
        self.index = index
        self.distance = distance

    #Ordenando ciudades
    def __lt__(self, other):
        return self.distance < other.distance


#Obtenga la mejor solución por distancia
def get_best_solution_by_distance(matrix: [], home: int):
    # Variables
    route = []
    from_index = home
    length = len(matrix) - 1
    # Recorre hasta completar ruta
    while len(route) < length:
        #Obtenner una matriz de fil
        row = matrix[from_index]
        # Creando lista con las ciudades
        cities = {}
        for i in range(len(row)):
            cities[i] = City(i, row[i])
        # Eliminar ciudades que ya están asignadas a la ruta
        del cities[home]
        for i in route:
            del cities[i]
        # Ordenar ciudades
        sorted = list(cities.values())
        sorted.sort()
        # Añadir la ciudad con la distancia más corta
        from_index = sorted[0].index
        route.append(from_index)
    # Crear un nuevo estado y actualizar la distancia
    state = State(route)
    state.update_distance(matrix, home)
    # Retornar estado
    return state


# Mutar una solución
def mutate(matrix: [], home: int, state: State, mutation_rate: float = 0.01):
    # Creando una copia del estado
    mutated_state = state.deepcopy()
    # Recorre todos los estados en una ruta
    for i in range(len(mutated_state.route)):
        # CComprueba si deberíamos hacer una mutación
        if (random.random() < mutation_rate):
            # Intercambiar 2 ciudades
            j = int(random.random() * len(state.route))
            city_1 = mutated_state.route[i]
            city_2 = mutated_state.route[j]
            mutated_state.route[i] = city_2
            mutated_state.route[j] = city_1
    # Actualizar la distancia
    mutated_state.update_distance(matrix, home)
    # Devolver estado mutado
    return mutated_state


# Algoritmo Hill climbing
def hill_climbing(matrix: [], home: int, initial_state: State, max_iterations: int, mutation_rate: float = 0.01):
    # Mantenga un registro del mejor estado
    best_state = initial_state
    #Se puede usar un iterador para darle al algoritmo más tiempo para encontrar una solucion
    iterator = 0
    # Creando un bucle infinitoooo
    while True:
        # Muta el mejor estado
        neighbor = mutate(matrix, home, best_state, mutation_rate)
        # Comprueba si la distancia es menor que en el mejor estado
        if (neighbor.distance >= best_state.distance):
            iterator += 1
            if (iterator > max_iterations):
                break
        if (neighbor.distance < best_state.distance):
            best_state = neighbor
    # Deuelve el mejor estado
    return best_state


def main():
    # Ciudades a viajar
    cities = ['Magdalena', 'San_Isidro', 'Cercado_de_Lima', 'Breña', 'Miraflores','San Miguel']
    city_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # Inicio
    home = 2  # Chicago
    # Maxima iteraciones
    max_iterations = 1000
    matrix= [
        [0, 2451, 713, 1018, 1631],
        [2451, 0, 1745, 1524, 831],
        [713, 1745, 0, 355, 920],
        [1018, 1524, 355, 0, 700],
        [1631, 831, 920, 700, 0]
    ]

    matrix2 = [
        [0, 130, 160, 210, 402],
        [125, 0, 190, 150, 201],
        [135, 186, 0, 340, 320],
        [145, 195, 231, 0, 154],
        [178, 245, 235, 322, 0]
    ]

    #Hill Climbing para encontrar una mejor solución
    state = get_best_solution_by_distance(matrix, home)
    state = hill_climbing(matrix, home, state, 1000, 0.1)
    print('-- Hill climbing solution --')
    print(cities[home], end='')
    for i in range(0, len(state.route)):
        print(' -> ' + cities[state.route[i]], end='')
    print(' -> ' + cities[home], end='')
    print('\n\nTotal distance: {0} km'.format(state.distance))

main()