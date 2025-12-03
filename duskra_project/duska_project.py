"""Input data"""
import csv
def read_file_for_graph(filename: str):

    lst = []
    with open(filename, 'r', encoding='utf-8') as file:

        lines = csv.reader(file)
        cities = next(lines)[1:]
        for el in lines:
            lst.append([int(elem) for elem in el[1:]])

    return (cities, lst)


def read_file_for_vehicles(filename: str):

    dictionary = {}
    with open(filename, 'r', encoding='utf-8') as file:

        lines = csv.reader(file)
        for kg, counter in lines:
            dictionary.setdefault(int(kg), int(counter))
    return dictionary


def read_file_for_packeges(filename: str):

    dictionary = {}
    with open(filename, 'r', encoding='utf-8') as file:

        lines = csv.reader(file)
        for kg, counter in lines:
            dictionary.setdefault(int(kg), int(counter))
    return dictionary


print(read_file_for_vehicles('vehicles.csv'))
print(read_file_for_packeges('packages.csv'))
print(read_file_for_graph('graph.csv'))
