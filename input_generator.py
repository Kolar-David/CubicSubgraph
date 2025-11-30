import random

V = 200
E = V*(V-1)/2

output_file_name = "input.in"

def standardize(u, v):
    return min(u, v), max(u, v)

def random_relabel(edges):
    vertices = [i for i in range(V)]

    permuted = vertices[:]
    random.shuffle(permuted)

    new_edges = [(permuted[u], permuted[v]) for (u, v) in edges]

    return new_edges

def valid_subgraph(edges):
    for i in range(0, 3):
        for j in range(4, 7):
            edges.add(standardize(i, j))
    return edges

def add_random_edges(edges):
    while len(edges) < E:
        u = random.randint(0, V-1)
        v = random.randint(0, V-1)
        if (u == v):
            continue
        edges.add(standardize(u, v))
    return edges

def add_line(edges, start, end):
    for i in range(start, end+1):
        if (i < end):
            edges.add(standardize(i, i+1))
    return edges


def output(edges):
    with open(output_file_name, "w") as f:
        f.write(f"{V} {len(edges)}\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")

def generate_line_graph():
    edges = set()
    edges = valid_subgraph(edges)
    edges = add_line(edges, 7, V-1)
    edges = random_relabel(list(edges))
    output(edges)

def generate_random_graph():
    edges = set()
    edges = valid_subgraph(edges)
    edges = add_random_edges(edges)
    edges = random_relabel(list(edges))
    output(edges)

generate_random_graph()