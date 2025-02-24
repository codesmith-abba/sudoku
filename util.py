import random
import math

def f(x):
    return -(x - 3)**2 + 10

def hill_climb(start, step_size=0.1, max_iter=10000):
    current_x = start
    current_value = f(current_x)

    for _ in range(max_iter):
        print(f"Current X: {current_x:.5f}")
        print(f"Current Value: {current_value:.5f}")
        # neighbors
        next_x1 = current_x + step_size
        next_x2 = current_x - step_size

        # Evaluate function at neighbors
        next_val1 = f(next_x1)
        next_val2 = f(next_x2)

        if next_val1 > current_value:
            current_x, current_value = next_x1, next_val1
        elif next_val2 > current_value:
            current_x, current_value = next_x2, next_val2
        else:
            break
    
    return current_x, current_value


start = random.uniform(-10, 10)
optimal_x, optimal_f = hill_climb(start)
print((round(optimal_x, 5), round(optimal_f, 5)))

# Define a set of cities with (x, y) coordinates
cities = {
    'A': (2, 3),
    'B': (5, 7),
    'C': (9, 2),
    'D': (3, 8),
    'E': (6, 4)
}

def distance(city1, city2):
    """Calculate Euclidean distance between two cities"""
    x1, y1 = cities[city1]
    x2, y2 = cities[city2]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def total_distance(tour):
    """Calculate total distance of the tour"""
    return sum(distance(tour[i], tour[i+1]) for i in range(len(tour) - 1)) + distance(tour[-1], tour[0])

def hill_climb_tsp(initial_tour, max_iterations=1000):
    """
    Hill Climbing for TSP
    - Starts with an initial tour and improves it by swapping cities
    """
    current_tour = initial_tour
    current_distance = total_distance(current_tour)

    for _ in range(max_iterations):
        # Generate a neighboring tour by swapping two cities
        new_tour = current_tour[:]
        i, j = random.sample(range(len(cities)), 2)  # Pick two random cities to swap
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

        # Calculate new distance
        new_distance = total_distance(new_tour)

        # Move to the better solution
        if new_distance < current_distance:
            current_tour, current_distance = new_tour, new_distance

    return current_tour, current_distance

# Start with a random tour
initial_tour = list(cities.keys())
random.shuffle(initial_tour)

optimal_tour, optimal_distance = hill_climb_tsp(initial_tour)

print(f"Optimal Tour: {optimal_tour}")
print(f"Optimal Distance: {optimal_distance:.2f}")
