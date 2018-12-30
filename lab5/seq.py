import copy

best_solution = 1000000
solution = []

def calculate_distance(routes, taken_edges):
    distance = 0
    for v1, edges in taken_edges.items():
        distance += sum([routes[v1][a[0]] for a in filter(lambda x: taken_edges[v1][x[0]] != 0, edges.items())])
    return distance/2

def compute(routes, taken_edges, distance, v1, taken_vertices, left_vertices):
    global best_solution
    global solution

    if distance > best_solution:
        return

    print("ENTER: " + str(v1))
    print(left_vertices)
    print(taken_edges)
    sv, sd = sorted(filter(lambda x: taken_edges[v1][x[0]] == 1, routes[v1].items()), key=lambda x: x[1])[0]
    taken_edges[v1][sv] = 0
    distance -= sd/2

    if not left_vertices:
        sv, sd = sorted(filter(lambda x: taken_edges[taken_vertices[0]][x[0]] == 1, routes[taken_vertices[0]].items()), key=lambda x: x[1])[0]
        distance -= sd/2
        distance += routes[v1][taken_vertices[0]]
        taken_vertices.append(taken_vertices[0])
        if distance < best_solution:
            print("Set solution")
            best_solution = distance
            solution = taken_vertices
        return

    for v2 in set(routes[v1].keys()).intersection(set(left_vertices)):
        sv, sd = sorted(filter(lambda x: taken_edges[v2][x[0]] == 1, routes[v2].items()), key=lambda x: x[1])[0]
        taken_edges[v2][sv] = 0
        compute(routes, copy.deepcopy(taken_edges), distance - sd/2 + routes[v1][v2], v2, taken_vertices + [v2], [x for x in left_vertices if x != v2])
        taken_edges[v2][sv] = 1
        

routes = {0: {1 : 10, 2 : 15, 3 : 20},
          1: {0 : 10, 2 : 35, 3 : 25},
          2: {0 : 15, 1 : 35, 3 : 30},
          3: {0 : 20, 1 : 25, 2 : 30}}

taken_edges = {0: {1 : 0, 2 : 0, 3 : 0},
               1: {0 : 0, 2 : 0, 3 : 0},
               2: {0 : 0, 1 : 0, 3 : 0},
               3: {0 : 0, 1 : 0, 2 : 0}}

#Take two shortest edges for every vertex
for v1, edges in routes.items():
    for v2, _ in sorted(filter(lambda x: taken_edges[v1][x[0]] == 0, edges.items()), key=lambda x: x[1])[0:2]:
        taken_edges[v1][v2] = 1

lower_bound = calculate_distance(routes, taken_edges)
print("Lower bound: " + str(lower_bound))

root_node = 0
compute(routes, copy.deepcopy(taken_edges), lower_bound, root_node, [root_node], [x for x in routes.keys() if x != root_node])

print("Result:")
print(solution)
print(best_solution)
