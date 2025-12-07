def load_hypergraph(path: str) -> tuple[int,  dict[int, set[int]], dict[int, set[int]]]:
    d = {}
    edges = {}
    with open(path, 'r', encoding='utf-8') as file:
        num = file.readline().rstrip()
        lines = file.readlines()
        lst = [i for i in range(int(num))]

        for i, elem in enumerate(lines):
            elem = elem.lstrip('{').rstrip('}\n')
            elem = elem.split(',')
            elem = [int(el) for el in elem]
            lines[i] = set(elem)
            edges[i+1] = set(elem)
        for n in lst:
            d[n] = set()
            for ind, el in enumerate(lines):
                if n in el:
                    d[n].add(ind + 1)

    return (int(num), d, edges)


def save_hypergraph(hg: tuple[int,  dict[int, set[int]], dict[int, set[int]]], path: str):
    with open(path, 'w', encoding='utf-8') as file:
        n, _, edges = hg
        file.write(str(n) + '\n')
        for el in edges.values():
            el = sorted(list(el))
            file.write('{')
            for i, elem in enumerate(el):
                if i == len(el) - 1:
                    file.write(str(elem) + '}')
                else:
                    file.write(str(elem) + ',')

def rewrite_hypergraph_rule1(hg: tuple[int,  dict[int, set[int]], dict[int, set[int]]]) -> tuple[int,  dict[int, set[int]], dict[int, set[int]]]:

    n, d, edges = hg
    existing_edges = {frozenset(v): k for k, v in edges.items()}
    next_edge_id = max(edges.keys()) + 1 if edges else 1
    for y in range(n):
        incident_edge_ids = d[y]
        binary_edge_ids = []
        for e_id in incident_edge_ids:
            if len(edges[e_id]) == 2:
                binary_edge_ids.append(e_id)
        num_binary = len(binary_edge_ids)

        for i in range(num_binary):
            for j in range(i + 1, num_binary):
                e1_id = binary_edge_ids[i]
                e2_id = binary_edge_ids[j]
                e1_vertices = edges[e1_id]
                e2_vertices = edges[e2_id]
                x = next(iter(e1_vertices - {y}))
                z = next(iter(e2_vertices - {y}))
                new_edge_vertices_fs = frozenset({x, z})
                if x == z:
                    continue
                if new_edge_vertices_fs not in existing_edges:
                    new_edge_set = set({x, z})
                    edges[next_edge_id] = new_edge_set
                    d[x].add(next_edge_id)
                    d[z].add(next_edge_id)
                    existing_edges[new_edge_vertices_fs] = next_edge_id
                    next_edge_id += 1

    return (n, d, edges)

def rewrite_hypergraph_rule2(hg: tuple[int, dict[int, set[int]], dict[int, set[int]]]) -> tuple[int, dict[int, set[int]], dict[int, set[int]]]:

    n, d, edges = hg
    next_edge_id = max(edges.keys()) + 1 if edges else 1
    edges_to_remove = set()
    new_common_sets = []
    ternary_edge_ids = [e_id for e_id, vertices in edges.items() if len(vertices) == 3]

    num_ternary = len(ternary_edge_ids)
    for i in range(num_ternary):
        e1_id = ternary_edge_ids[i]
        e1_vertices = edges.get(e1_id)
        if e1_id in edges_to_remove:
            continue

        for j in range(i + 1, num_ternary):
            e2_id = ternary_edge_ids[j]
            e2_vertices = edges.get(e2_id)

            if e2_id in edges_to_remove:
                continue
            common_set = e1_vertices.intersection(e2_vertices)

            if len(common_set) == 2:

                z_set = e1_vertices - common_set
                w_set = e2_vertices - common_set

                if z_set != w_set:
                    new_common_sets.append(common_set)
                    edges_to_remove.add(e1_id)
                    edges_to_remove.add(e2_id)
                    break

    if not edges_to_remove:
        return (n, d, edges)

    for e_id in edges_to_remove:
        vertices = edges.pop(e_id, set())
        for v in vertices:
            d[v].discard(e_id)
    for common_set in new_common_sets:
        f = n
        n += 1
        d[f] = set()
        new_edge_vertices = common_set.union({f})
        edges[next_edge_id] = new_edge_vertices

        for v in new_edge_vertices:
            d[v].add(next_edge_id)
        next_edge_id += 1

    return (n, d, edges)

print(load_hypergraph('graph1'))
