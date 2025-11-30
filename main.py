import subprocess
from argparse import ArgumentParser

K = 3

def parse_int_line(line):
    return [int(i) for i in line.split()]

def load_input(file_name):
    # to translate edges to corresponding integers and vice versa
    edges_to_int = dict()
    int_to_edges = [None]

    index = 1
    with open(file_name, "r") as file:
        first = True
        for line in file:
            if first:
                first = False
                V, E = parse_int_line(line)
                graph = [[] for _ in range(V)]
                continue
            u, v = parse_int_line(line)
            edges_to_int[(u, v)] = index
            edges_to_int[(v, u)] = index
            int_to_edges.append((u, v))
            graph[u].append(v)
            graph[v].append(u)
            index += 1

    return V, E, int_to_edges, edges_to_int, graph

def implication_with_ands_on_left_to_cnf(left_ls, right_ls):
    return [[*[-x for x in left_ls], *right_ls]]

def encode_1_vertex(v, base, edges_to_int, graph):
    cnf = []

    def var(i, count):
        return base + i*(K+2) + count

    d = len(graph[v])

    if d == 0:
        return base, cnf

    # var(0, c) = True only for c=0
    cnf.append([var(0, 0)])
    for c in range(1, K+2):
        cnf.append([-var(0, c)])

    for i, neighbor in enumerate(graph[v]):
        edge_index = edges_to_int[(v, neighbor)]

        for c in range(0, K+1):
            to_state = var(i+1, c+1)
            # var(i, c) ^ e_i => var(i+1, c+1)
            cnf.extend(implication_with_ands_on_left_to_cnf([var(i, c), edge_index], [to_state]))
            # var(i, c) ^ not e_i => var(i+1, c)
            cnf.extend(implication_with_ands_on_left_to_cnf([var(i, c), -edge_index], [var(i + 1, c)]))

        # var(i, K+1) => var(i+1, K+1)
        cnf.extend(implication_with_ands_on_left_to_cnf([var(i, K + 1)], [var(i + 1, K + 1)]))

    # check if d is 0 or K and nothing else
    cnf.append([var(d, 0), var(d, K)])
    for j in range(0, K+2):
        if j not in (0, K):
            cnf.append([-var(d, j)])

    new_base = var(d, K+1) + 1
    return new_base, cnf

def call_solver(cnf, nr_vars, output_name, solver_name, verbosity):
    with open(output_name, "w") as file:
        file.write(f"p cnf {nr_vars} {len(cnf)}\n")
        for clause in cnf:
            file.write(" ".join(str(lit) for lit in clause) + " 0\n")

    return subprocess.run(['./' + solver_name, '-model', '-verb=' + str(verbosity), output_name], stdout=subprocess.PIPE)


def encode(V, E, edges_to_int, graph):
    # 1 item = 1 clause
    cnf = []

    # We need to pick at least 1 edge
    cnf.append([i for i in range(1, E+1)])

    base = E+1

    for v in range(V):
        base, clauses = encode_1_vertex(v, base, edges_to_int, graph)
        cnf.extend(clauses)

    num_variables = base - 1
    return cnf, num_variables

def print_result(result, int_to_edges, E):
    for line in result.stdout.decode('utf-8').split('\n'):
        print(line)

    if result.returncode == 20:
        return

    model = []
    for line in result.stdout.decode('utf-8').split('\n'):
        if line.startswith("v"):
            vars_ = line.split()
            vars_.remove("v")
            model.extend(int(v) for v in vars_)
    if 0 in model:
        model.remove(0)

    model_set = set(model)

    print()
    print("##################################################################")
    print("############[ Human readable result ]###########")
    print("##################################################################")
    print()

    kept = []
    removed = []

    for idx in range(1, E + 1):
        u, v = int_to_edges[idx]
        if idx in model_set:
            kept.append((u, v))
        else:
            removed.append((u, v))

    print(f"Edges kept in the final graph (degree 0 or {K} at every vertex):")
    for u, v in kept:
        print(u, v)

    #print(f"Edges removed from the final graph:")
    #for u, v in removed:
    #    print(u, v)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        default="input.in",
        type=str,
        help="The instance file (graph). First line: V E, then E lines: u v."
    )
    parser.add_argument(
        "-o",
        "--output",
        default="formula.cnf",
        type=str,
        help="Output file for the DIMACS CNF formula."
    )
    parser.add_argument(
        "-s",
        "--solver",
        default="glucose-syrup",
        type=str,
        help="The SAT solver to be used."
    )
    parser.add_argument(
        "-v",
        "--verb",
        default=1,
        type=int,
        choices=range(0, 2),
        help="Verbosity of the SAT solver used."
    )

    args = parser.parse_args()
    V, E, int_to_edges, edges_to_int, graph = load_input(args.input)
    cnf, nr_vars = encode(V, E, edges_to_int, graph)
    result = call_solver(cnf, nr_vars, args.output, args.solver, args.verb)
    print_result(result, int_to_edges, E)