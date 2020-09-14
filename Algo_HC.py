# Import libraries
import random
import copy

# This class represent a state
class State:
    # Create a new state
    def __init__(self, route: [], distance: int = 0):
        self.route = route
        self.distance = distance

    # Compare states
    def __eq__(self, other):
        for i in range(len(self.route)):
            if (self.route[i] != other.route[i]):
                return False
        return True

    # Sort states
    def __lt__(self, other):
        return self.distance < other.distance

    # Print a state
    def __repr__(self):
        return ('({0},{1})\n'.format(self.route, self.distance))

    # Create a shallow copy
    def copy(self):
        return State(self.route, self.distance)

    # Create a deep copy
    def deepcopy(self):
        return State(copy.deepcopy(self.route), copy.deepcopy(self.distance))

    # Update distance
    def update_distance(self, matrix, home):

        # Reset distance
        self.distance = 0
        # Keep track of departing city
        from_index = home
        # Loop all cities in the current route
        for i in range(len(self.route)):
            self.distance += matrix[from_index][self.route[i]]
            from_index = self.route[i]
        # Add the distance back to home
        self.distance += matrix[from_index][home]


# This class represent a city (used when we need to delete cities)
class City:
    # Create a new city
    def __init__(self, index: int, distance: int):
        self.index = index
        self.distance = distance

    # Sort cities
    def __lt__(self, other):
        return self.distance < other.distance


# Get the best random solution from a population
def get_random_solution(matrix: [], home: int, city_indexes: [], size: int, use_weights=False):
    # Create a list with city indexes
    cities = city_indexes.copy()
    # Remove the home city
    cities.pop(home)
    # Create a population
    population = []
    for i in range(size):
        if (use_weights == True):
            state = get_random_solution_with_weights(matrix, home)
        else:
            # Shuffle cities at random
            random.shuffle(cities)
            # Create a state
            state = State(cities[:])
            state.update_distance(matrix, home)
        # Add an individual to the population
        population.append(state)
    # Sort population
    population.sort()
    # Return the best solution
    return population[0]


# Get best solution by distance
def get_best_solution_by_distance(matrix: [], home: int):
    # Variables
    route = []
    from_index = home
    length = len(matrix) - 1
    # Loop until route is complete
    while len(route) < length:
        # Get a matrix row
        row = matrix[from_index]
        # Create a list with cities
        cities = {}
        for i in range(len(row)):
            cities[i] = City(i, row[i])
        # Remove cities that already is assigned to the route
        del cities[home]
        for i in route:
            del cities[i]
        # Sort cities
        sorted = list(cities.values())
        sorted.sort()
        # Add the city with the shortest distance
        from_index = sorted[0].index
        route.append(from_index)
    # Create a new state and update the distance
    state = State(route)
    state.update_distance(matrix, home)
    # Return a state
    return state


# Get a random solution by using weights
def get_random_solution_with_weights(matrix: [], home: int):
    # Variables
    route = []
    from_index = home
    length = len(matrix) - 1
    # Loop until route is complete
    while len(route) < length:
        # Get a matrix row
        row = matrix[from_index]
        # Create a list with cities
        cities = {}
        for i in range(len(row)):
            cities[i] = City(i, row[i])
        # Remove cities that already is assigned to the route
        del cities[home]
        for i in route:
            del cities[i]
        # Get the total weight
        total_weight = 0
        for key, city in cities.items():
            total_weight += city.distance
        # Add weights
        weights = []
        for key, city in cities.items():
            weights.append(total_weight / city.distance)
        # Add a city at random
        from_index = random.choices(list(cities.keys()), weights=weights)[0]
        route.append(from_index)
    # Create a new state and update the distance
    state = State(route)
    state.update_distance(matrix, home)
    # Return a state
    return state


# Mutate a solution
def mutate(matrix: [], home: int, state: State, mutation_rate: float = 0.01):
    # Create a copy of the state
    mutated_state = state.deepcopy()
    # Loop all the states in a route
    for i in range(len(mutated_state.route)):
        # Check if we should do a mutation
        if (random.random() < mutation_rate):
            # Swap two cities
            j = int(random.random() * len(state.route))
            city_1 = mutated_state.route[i]
            city_2 = mutated_state.route[j]
            mutated_state.route[i] = city_2
            mutated_state.route[j] = city_1
    # Update the distance
    mutated_state.update_distance(matrix, home)
    # Return a mutated state
    return mutated_state


# Hill climbing algorithm
def hill_climbing(matrix: [], home: int, initial_state: State, max_iterations: int, mutation_rate: float = 0.01):
    # Keep track of the best state
    best_state = initial_state
    # An iterator can be used to give the algorithm more time to find a solution
    iterator = 0
    # Create an infinite loop
    while True:
        # Mutate the best state
        neighbor = mutate(matrix, home, best_state, mutation_rate)
        # Check if the distance is less than in the best state
        if (neighbor.distance >= best_state.distance):
            iterator += 1
            if (iterator > max_iterations):
                break
        if (neighbor.distance < best_state.distance):
            best_state = neighbor
    # Return the best state
    return best_state


# The main entry point for this module
def main():
    # Cities to travel
    cities = ['New York', 'Los Angeles', 'Chicago', 'Minneapolis', 'Denver', 'Dallas', 'Seattle', 'Boston',
              'San Francisco', 'St. Louis', 'Houston', 'Phoenix', 'Salt Lake City']
    city_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # Index of start location
    home = 2  # Chicago
    # Max iterations
    max_iterations = 1000
    # Distances in miles between cities, same indexes (i, j) as in the cities array
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

    # Run hill climbing to find a better solution
    state = get_best_solution_by_distance(matrix, home)
    state = hill_climbing(matrix, home, state, 1000, 0.1)
    print('-- Hill climbing solution --')
    print(cities[home], end='')
    for i in range(0, len(state.route)):
        print(' -> ' + cities[state.route[i]], end='')
    print(' -> ' + cities[home], end='')
    print('\n\nTotal distance: {0} miles'.format(state.distance))


# Tell python to run main method
if __name__ == "__main__": main()