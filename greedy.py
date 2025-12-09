'''Greddy algorihtm'''

INF = float('inf')

def calculate_greedy_truck_route(start_node, packages_in_truck, dist_matrix):
    """
    Greedy TSP (Nearest Neighbour).
    Works fast, but is not the most efficient.

    :param start_node: Starting point (Warehouse).
    :param packages_in_truck: List of packages currently loaded in the truck.
    :param dist_matrix: Matrix of distances between cities.
    :return: Tuple (minimum_distance, list_of_cities_in_route).
    """
    if not packages_in_truck:
        return 0, []

    destinations = list(set(p['destination'] for p in packages_in_truck))

    if not destinations:
        return 0, [start_node, start_node]

    current_city = start_node
    unvisited = set(destinations)
    route = [start_node]
    total_distance = 0

    while unvisited:
        best_next = None
        best_dist = INF

        for city in unvisited:
            d = dist_matrix[current_city].get(city, INF)
            if d < best_dist:
                best_dist = d
                best_next = city

        if best_next is None or best_dist == INF:
            return INF, []

        total_distance += best_dist
        route.append(best_next)
        unvisited.remove(best_next)
        current_city = best_next

    return_to_start = dist_matrix[current_city].get(start_node, INF)
    if return_to_start == INF:
        return INF, []

    total_distance += return_to_start
    route.append(start_node)

    return total_distance, route
