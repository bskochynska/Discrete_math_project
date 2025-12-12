"""
This module implements a solution for the Capacitated Vehicle Routing Problem (CVRP),
designed to find the mathematically optimal delivery schedule for a fleet of vehicles.

Key Algorithms
--------------
1. **Dijkstra's Algorithm**:
   Used to compute the precise shortest paths between cities on a weighted road graph.
   This ensures that the "distance matrix" reflects real-world road network constraints.

2. **Traveling Salesperson Problem (TSP) - Brute Force**:
   Generates all possible route permutations ($N!$) for a specific set of packages
   to find the strictly minimal travel distance for a single truck.


Input Requirements (CSV)
------------------------
The script requires three CSV files in the working directory:
1. `graph.csv`    : Road network (Format: `PointA, PointB, Distance`).
2. `vehicles.csv` : Fleet specifications (Format: `Capacity, Count`).
3. `packages.csv` : Delivery orders (Format: `Weight, Destination, Count`).

"""
import argparse
from copy import deepcopy
from greedy import calculate_greedy_truck_route
from data_input import read_packages
from data_input import read_vehicles
from data_input import read_graph
from visualization import animate_delivery

INF = float('inf')

def get_permutations(elements):
    """
    Generator for list permutations (similar to itertools.permutations).
    Uses recursion to generate all possible orders of elements.

    :param elements: List of elements to permute.
    :return: Generator yielding lists with permutations.

    >>> list(get_permutations([1, 2]))
    [[1, 2], [2, 1]]
    >>> list(get_permutations([]))
    [[]]
    >>> list(get_permutations([1]))
    [[1]]
    """
    if len(elements) <= 1:
        yield elements
        return
    for i, current in enumerate(elements):
        remaining = elements[:i] + elements[i+1:]
        for p in get_permutations(remaining):
            yield [current] + p

def dijkstra(graph, start_node):
    """
    Implements Dijkstra's algorithm to find shortest paths from a start node to all others.

    :param graph: Adjacency dictionary {node: {neighbor: weight, ...}}.
    :param start_node: The starting node.
    :return: Dictionary {node: distance} representing shortest paths.

    >>> g = {'A': {'B': 10, 'C': 3}, 'B': {'C': 1, 'D': 2}, 'C': {'B': 4, 'D': 8}, 'D': {}}
    >>> dists = my_dijkstra(g, 'A')
    >>> dists['A']
    0
    >>> dists['B']
    7
    >>> dists['D']
    9
    """
    distances = {node: INF for node in graph}
    distances[start_node] = 0
    visited = set()
    nodes = list(graph.keys())

    while True:
        min_node = None
        min_val = INF
        for node in nodes:
            if node not in visited and distances[node] < min_val:
                min_val = distances[node]
                min_node = node
        if min_node is None:
            break
        visited.add(min_node)
        for neighbor, weight in graph[min_node].items():
            if distances[min_node] + weight < distances[neighbor]:
                distances[neighbor] = distances[min_node] + weight
    return distances

def get_full_dist_matrix(graph, points):
    """
    Builds a matrix (dict of dicts) of shortest distances between all points of interest.
    Uses Dijkstra's algorithm for each starting point.

    :param graph: The road graph.
    :param points: List of city names to include in the matrix.
    :return: Dictionary {start: {end: distance}}.

    >>> g = {'Kyiv': {'Lviv': 500}, 'Lviv': {'Kyiv': 500}}
    >>> m = get_full_dist_matrix(g, ['Kyiv', 'Lviv'])
    >>> m['Kyiv']['Lviv']
    500
    >>> m['Lviv']['Kyiv']
    500
    """
    matrix = {}
    for start in points:
        if start not in graph:
            matrix[start] = {end: INF for end in points}
        else:
            dists = dijkstra(graph, start)
            matrix[start] = {}
            for end in points:
                matrix[start][end] = dists.get(end, INF)
    return matrix

def calculate_optimal_truck_route(start_node, packages_in_truck, dist_matrix):
    """
    Solves the Traveling Salesperson Problem (TSP) for a single truck using brute force.
    Finds the visitation order with the minimum total distance.

    :param start_node: Starting point (Warehouse).
    :param packages_in_truck: List of packages currently loaded in the truck.
    :param dist_matrix: Matrix of distances between cities.
    :return: Tuple (minimum_distance, list_of_cities_in_route).

    >>> matrix = {'K': {'K': 0, 'L': 10}, 'L': {'K': 10, 'L': 0}}
    >>> packs = [{'destination': 'L'}]
    >>> dist, route = calculate_optimal_truck_route('K', packs, matrix)
    >>> dist
    20
    >>> route
    ['K', 'L', 'K']
    """
    if not packages_in_truck:
        return 0, []
    destinations = list(set(p['destination'] for p in packages_in_truck))

    if not destinations:
        return 0, [start_node, start_node]
    min_dist = INF
    best_route = []

    for perm in get_permutations(destinations):
        route = [start_node] + perm + [start_node]
        d = 0
        valid = True
        for i in range(len(route) - 1):
            dist = dist_matrix.get(route[i], {}).get(route[i+1], INF)
            if dist == INF:
                valid = False
                break
            d += dist
        if valid and d < min_dist:
            min_dist = d
            best_route = route

    return min_dist, best_route

def find_optimal_delivery_plan(package_idx, vehicles, packages, warehouse, dist_matrix, current_best_solution):
    """
    Main recursive function to solve the CVRP (Capacitated Vehicle Routing Problem).
    Distributes packages among vehicles and searches for the global minimum distance
    using backtracking.

    Modifies the dictionary `current_best_solution`.

    :param package_idx: Index of the current package being processed.
    :param vehicles: List of vehicles (with their current state).
    :param packages: List of all packages.
    :param warehouse: Name of the warehouse city.
    :param dist_matrix: Distance matrix.
    :param current_best_solution: Dictionary to store the best result found so far.
    """
    if package_idx == len(packages):
        current_total_dist = 0
        current_vehicles_res = []
        possible_config = True

        for v in vehicles:
            if not v['packages']:
                continue
            destinations = set(p['destination'] for p in v['packages'])
            tsp_solver = choose_tsp_solver(len(destinations))

            d, route = tsp_solver(warehouse, v['packages'], dist_matrix)

            if d == INF:
                possible_config = False
                break

            v_copy = v.copy()
            v_copy['route_dist'] = d
            v_copy['optimal_route'] = route
            current_vehicles_res.append(v_copy)
            current_total_dist += d

        if possible_config and current_total_dist < current_best_solution['total_distance']:
            current_best_solution['total_distance'] = current_total_dist
            current_best_solution['vehicles'] = deepcopy(current_vehicles_res)
            current_best_solution['unassigned'] = []
        return

    pkg = packages[package_idx]
    is_placed = False

    for i, vehicle in enumerate(vehicles):
        if i > 0 and not vehicle['packages'] and not vehicles[i-1]['packages'] and vehicle['capacity'] == vehicles[i-1]['capacity']:
            continue

        if vehicle['load'] + pkg['weight'] <= vehicle['capacity']:
            vehicle['packages'].append(pkg)
            vehicle['load'] += pkg['weight']
            find_optimal_delivery_plan(package_idx + 1, vehicles, packages, warehouse, dist_matrix, current_best_solution)
            vehicle['load'] -= pkg['weight']
            vehicle['packages'].pop()
            is_placed = True

    if not is_placed:
        find_optimal_delivery_plan(package_idx + 1, vehicles, packages, warehouse, dist_matrix, current_best_solution)

def choose_tsp_solver(num_destinations):
    """
    Returns the function to use for TSP depending on number of destinations.
    """
    if num_destinations <= 10:
        return calculate_optimal_truck_route
    else:
        return calculate_greedy_truck_route

def main():
    """
    Main entry point.
    Reads data using argparse, executes the algorithm, and prints the results.
    """

    parser = argparse.ArgumentParser(description="Optimal Logistics Routing Script")
    parser.add_argument("graph_file", help="Path to the graph CSV file (e.g., graph.csv)")
    parser.add_argument("vehicles_file", help="Path to the vehicles CSV file (e.g., vehicles.csv)")
    parser.add_argument("packages_file", help="Path to the packages CSV file (e.g., packages.csv)")
    parser.add_argument("--warehouse", default="Kyiv", help="Name of the warehouse city (default: Kyiv)")
    parser.add_argument("--viz", action="store_true", help="Увімкнути візуалізацію")

    args = parser.parse_args()

    try:
        graph = read_graph(args.graph_file)
        vehicles = read_vehicles(args.vehicles_file)
        packages = read_packages(args.packages_file)
    except FileNotFoundError as e:
        print(f"Error reading file: {e}")
        return

    warehouse_location = args.warehouse
    all_points = {warehouse_location}
    for p in packages:
        all_points.add(p['destination'])

    valid_points = [p for p in all_points if p in graph]

    if warehouse_location not in graph:
        print(f"Складу '{warehouse_location}' немає на мапі!")
        return

    if len(valid_points) != len(all_points):
        print("Не всі міста є на мапі!")

    dist_matrix = get_full_dist_matrix(graph, valid_points)

    print(f"Склад: {warehouse_location}")
    print(f"Пакунків: {len(packages)}, Вантажівок: {len(vehicles)}")

    best_solution = {
        'total_distance': INF,
        'vehicles': None,
        'unassigned': None
    }

    find_optimal_delivery_plan(0, vehicles, packages, warehouse_location, dist_matrix, best_solution)

    print("\n" + "="*50)
    print("Оптимальний результат(Мін. пальне)")
    print("="*50)

    if best_solution['total_distance'] == INF:
        print("Вантаж не влазить.")
    else:
        assigned_ids = set()
        for v in (best_solution['vehicles'] or []):
            print(f"\n{v['id']} [Завантажено: {v['load']}/{v['capacity']} кг]")
            route_str = " -> ".join(v['optimal_route'])
            print(f"Маршрут: {route_str}")
            print(f"Дистанція: {v['route_dist']} км")

            pack_list = []
            for p in v['packages']:
                pack_list.append(f"{p['weight']}кг({p['destination']})")
                assigned_ids.add(p['id'])
            print(f"Вантаж: {', '.join(pack_list)}")

        print("-" * 50)
        print(f"Загальна дистанція: {best_solution['total_distance']} км")
        unassigned = [p for p in packages if p['id'] not in assigned_ids]
        if unassigned:
            print(f"\nНе влізли: {sum(p['weight'] for p in unassigned)} кг")
        if args.viz and best_solution['vehicles']:
            animate_delivery(best_solution['vehicles'], graph, warehouse_location)

if __name__ == "__main__":
    main()
