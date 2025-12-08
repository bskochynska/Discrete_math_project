"""Input data"""
import csv
def read_graph(filename):
    """
    Reads the road graph from a CSV file.

    :param filename: Path to file (Format: PointA, PointB, Distance).
    :return: Adjacency dictionary {u: {v: w, ...}}.
    """
    graph = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            if len(row)<3 or not row[2].isdigit():
                continue
            u, v, w = row[0].strip(), row[1].strip(), int(row[2])
            if u not in graph:
                graph[u]={}
            if v not in graph:
                graph[v]={}
            graph[u][v]=w
            graph[v][u]=w
    return graph

def read_vehicles(filename):
    """
    Reads the vehicle fleet from a CSV file.

    :param filename: Path to file (Format: Capacity, Count).
    :return: List of vehicle dictionaries, sorted by capacity descending.
    """
    vehicles = []
    with open(filename, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            if not row[0].isdigit():
                continue
            capacity, count = int(row[0]), int(row[1])
            for i in range(count):
                vehicles.append({'id': f"Tr_{capacity}_{i+1}", 'capacity': capacity, 'load': 0, 'packages': []})
    vehicles.sort(key=lambda x: x['capacity'], reverse=True)
    return vehicles

def read_packages(filename):
    """
    Reads the list of orders (packages) from a CSV file.

    :param filename: Path to file (Format: Weight, City, Count(optional)).
    :return: List of packages, sorted by weight descending (Bin Packing heuristic).
    """
    packages = []
    package_id = 1
    with open(filename, 'r', encoding='utf-8',) as f:
        for row in csv.reader(f):
            if len(row)<2 or not row[0].isdigit():
                continue
            w, d = int(row[0]), row[1].strip()
            count = int(row[2]) if len(row)>2 else 1
            for _ in range(count):
                packages.append({'id': package_id, 'weight': w, 'destination': d})
                package_id+=1
    packages.sort(key=lambda x: x['weight'], reverse=True)
    return packages

print(read_vehicles('vehicles.csv'))
print(read_packages('packages.csv'))
print(read_graph('graph.csv'))
