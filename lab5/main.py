import pykka

def calculate_distance(routes, taken_edges):
    distance = 0
    for v1, edges in taken_edges.items():
        distance += sum([routes[v1][a[0]] for a in filter(lambda x: taken_edges[v1][x[0]] != 0, edges.items())])
    return distance/2


class TSPResolver(pykka.ThreadingActor):
    def __init__(self, my_arg=None):
        super(TSPResolver, self).__init__()
        ... # My optional init code with access to start() arguments

    def compute(routes, taken_edges, distance, taken_vertices):
        if distance > best_solution:
            return

        v1 = taken_vertices[-1]
        left_vertices = [x for x in routes.keys() if x not in taken_vertices]

        sv, sd = sorted(filter(lambda x: taken_edges[v1][x[0]] == 1, routes[v1].items()), key=lambda x: x[1])[0]
        taken_edges[v1][sv] = 0
        distance -= sd/2

        if not left_vertices:
            sv, sd = sorted(filter(lambda x: taken_edges[taken_vertices[0]][x[0]] == 1, routes[taken_vertices[0]].items()), key=lambda x: x[1])[0]
            distance -= sd/2
            distance += routes[v1][taken_vertices[0]]
            taken_vertices.append(taken_vertices[0])
            if distance < best_solution:
                best_solution = distance
                solution = taken_vertices
            return

        for v2 in set(routes[v1].keys()).intersection(set(left_vertices)):
            sv, sd = sorted(filter(lambda x: taken_edges[v2][x[0]] == 1, routes[v2].items()), key=lambda x: x[1])[0]
            taken_edges[v2][sv] = 0
            compute(routes, copy.deepcopy(taken_edges), distance - sd/2 + routes[v1][v2], taken_vertices + [v2])
            taken_edges[v2][sv] = 1

    def on_receive(self, message):
        ... # My optional message handling code for a plain actor

class TSPExecutor(pykka.ThreadingActor):
    def __init__(self, my_arg=None):
        super(TSPExecutor, self).__init__()

    def simple_compute(routes, taken_edges, distance, taken_vertices, depth=0):
        if distance > best_solution:
            return

        v1 = taken_vertices[-1]
        left_vertices = [x for x in routes.keys() if x not in taken_vertices]

        sv, sd = sorted(filter(lambda x: taken_edges[v1][x[0]] == 1, routes[v1].items()), key=lambda x: x[1])[0]
        taken_edges[v1][sv] = 0
        distance -= sd/2

        for v2 in set(routes[v1].keys()).intersection(set(left_vertices)):
            sv, sd = sorted(filter(lambda x: taken_edges[v2][x[0]] == 1, routes[v2].items()), key=lambda x: x[1])[0]
            taken_edges[v2][sv] = 0
            if depth < 1:
                simple_compute(routes, copy.deepcopy(taken_edges), distance - sd/2 + routes[v1][v2], taken_vertices + [v2])
            else:
                #Send message to worker
            taken_edges[v2][sv] = 1

        #Save state and return
