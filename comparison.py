"""
This module conducts a comparative analysis between two approaches to the
Traveling Salesperson Problem (TSP):
1. Exact Algorithm (Brute Force): Guarantees the shortest path but has factorial time complexity O(N!).
2. Greedy Algorithm (Nearest Neighbor): Provides an approximate solution with fast execution time O(N^2).
"""
import random
import time
import matplotlib.pyplot as plt

from main import calculate_optimal_truck_route
from greedy import calculate_greedy_truck_route

def generate_test_data(num_cities):
    """
    Generates a random distance matrix and mock packages for N cities.

    :param num_cities: Total number of cities (including the warehouse).
    :return: A tuple containing (start_node, packages_mock, dist_matrix).
    """
    cities = [f"City_{i}" for i in range(num_cities)]
    start_node = cities[0]
    dist_matrix = {city: {} for city in cities}
    for i in range(num_cities):
        for j in range(i, num_cities):
            city_a = cities[i]
            city_b = cities[j]

            if i == j:
                dist = 0
            else:
                dist = random.randint(10, 100)
            dist_matrix[city_a][city_b] = dist
            dist_matrix[city_b][city_a] = dist
    packages_mock = []
    for city in cities[1:]:
        packages_mock.append({
            'id': f"pkg_{city}",
            'destination': city,
            'weight': 100
        })

    return start_node, packages_mock, dist_matrix

def compare_algorithms():
    """
    Runs a comparative benchmark between Greedy and Brute Force TSP algorithms.
    Measures execution time and path distance for various problem sizes.
    """
    problem_sizes = [4, 6, 8, 9, 10, 11]
    # To observe the massive performance gap, add 12 or more cities.
    # and modify logic in 'main.py' that switches to Greedy automatically when N > 10.
    results = []
    for n in problem_sizes:
        start_node, packages, dist_matrix = generate_test_data(n)

        t_s = time.perf_counter()
        greedy_dist, _ = calculate_greedy_truck_route(start_node, packages, dist_matrix)
        t_f = time.perf_counter()
        greedy_time = t_f - t_s

        t_s = time.perf_counter()
        brute_dist, _ = calculate_optimal_truck_route(start_node, packages, dist_matrix)
        t_f = time.perf_counter()
        brute_time = t_f - t_s
        # if brute_time > 60:
        #     print("Very long calculating")
        # elif brute_time > 1:
        #     print("Lond calculating")

        if brute_dist > 0:
            gap = ((greedy_dist - brute_dist) / brute_dist) * 100
        else:
            gap = 0

        results.append({
            "n": n,
            "greedy_time": greedy_time,
            "brute_time": brute_time,
            "greedy_dist": greedy_dist,
            "brute_dist": brute_dist,
            "gap": gap
        })

        print(f"    ~~Кількість міст: {n} ~~")
        print(f">>> Точний:  {brute_dist} км  (за {brute_time:.6f} с)")
        print(f">>> Жадібний:  {greedy_dist} км  (за {greedy_time:.6f} с)")

        if gap == 0:
            print("Результат ідеальний! Різниця 0%")
        else:
            print(f"Жадібний помилився на {gap:.2f}% ({greedy_dist - brute_dist} км)")
    return results


def vis_resusts(results):
    """
    Visualizes the benchmark results using Matplotlib.
    """
    n = [r['n'] for r in results]
    greedy_time = [r['greedy_time'] for r in results]
    brute_time = [r['brute_time'] for r in results]
    gaps = [r['gap'] for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.plot(n, brute_time, marker='o', label='Brute Force(Exact)', color='red')
    ax1.plot(n, greedy_time, marker='x', label='Greedy', color='blue')
    ax1.set_title('Time Complexity Analysis')
    ax1.set_xlabel('Number of cities (n)')
    ax1.set_ylabel('Time (sec)')
    ax1.legend()
    ax1.grid(True)

    bars = ax2.bar(n, gaps, color='orange')
    ax2.set_title('Втрата якості жадібного алгоритму (%)')
    ax2.set_xlabel('Кількість міст (N)')
    ax2.set_ylabel('На скільки % маршрут довший за ідеал')
    ax2.set_ylim(bottom=0)
    ax2.grid(axis='y', linestyle='--')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    data = compare_algorithms()
    vis_resusts(data)
