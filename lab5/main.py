import pykka
import copy
import itertools
import random

def calculate_distance(routes, taken_edges):
    distance = 0
    for v1, edges in taken_edges.items():
        distance += sum([routes[v1][a[0]] for a in filter(lambda x: taken_edges[v1][x[0]] != 0, edges.items())])
    return distance/2

class TSPResolver(pykka.ThreadingActor):
    def __init__(self, executor, routes, taken_edges):
        super(TSPResolver, self).__init__()
        self.executor = executor
        self.routes = routes
        self.taken_edges = taken_edges
        self.best_solution = 100000000
        self.solution = []

    def on_start(self):
        msg = {
            'actor': self.actor_ref,
            'distance' : self.best_solution,
            'taken_vertices' : self.solution
        }
        self.executor.tell(msg)

    def on_receive(self, message):
        taken_edges = copy.deepcopy(self.taken_edges)
        taken_vertices = message['taken_vertices']
        distance = calculate_distance(self.routes, taken_edges)
        self.best_solution = message['best_solution']

        for v1, v2 in zip(taken_vertices, taken_vertices[1:]):
            sv, sd = sorted(filter(lambda x: taken_edges[v1][x[0]] == 1, routes[v1].items()), key=lambda x: x[1])[0]
            taken_edges[v1][sv] = 0
            distance -= sd/2

            sv, sd = sorted(filter(lambda x: taken_edges[v2][x[0]] == 1, routes[v2].items()), key=lambda x: x[1])[0]
            taken_edges[v2][sv] = 0
            distance -= sd/2

            distance += routes[v1][v2]
        self.compute(taken_edges, distance, taken_vertices)
        msg = {
            'actor': self.actor_ref,
            'distance': self.best_solution+1,
            'taken_vertices': self.solution
        }
        self.executor.tell(msg)

    def compute(self, taken_edges, distance, taken_vertices):
        if distance >= self.best_solution:
            return

        v1 = taken_vertices[-1]
        left_vertices = [x for x in self.routes.keys() if x not in taken_vertices]
        sv, sd = sorted(filter(lambda x: taken_edges[v1][x[0]] == 1, self.routes[v1].items()), key=lambda x: x[1])[0]
        taken_edges[v1][sv] = 0
        distance -= sd/2

        if not left_vertices:
            sv, sd = sorted(filter(lambda x: taken_edges[taken_vertices[0]][x[0]] == 1, routes[taken_vertices[0]].items()), key=lambda x: x[1])[0]
            distance -= sd/2
            distance += routes[v1][taken_vertices[0]]
            taken_vertices.append(taken_vertices[0])
            if distance < self.best_solution:
                self.best_solution = distance
                self.solution = taken_vertices
            return

        for v2 in set(self.routes[v1].keys()).intersection(set(left_vertices)):
            sv, sd = sorted(filter(lambda x: taken_edges[v2][x[0]] == 1, self.routes[v2].items()), key=lambda x: x[1])[0]
            taken_edges[v2][sv] = 0
            self.compute(copy.deepcopy(taken_edges), distance - sd/2 + self.routes[v1][v2], taken_vertices + [v2])
            taken_edges[v2][sv] = 1

class TSPExecutor(pykka.ThreadingActor):
    def __init__(self, routes, depth, taken_edges, root_node):
        super(TSPExecutor, self).__init__()
        vertices = [x for x in routes.keys()]
        self.tasks = [[root_node, x, y] for x in vertices for y in vertices if (x != y and x != root_node and y != root_node)]
        self.best_solution = 100000000
        self.solution = []
        self.sent = len(self.tasks)
        self.received = 0

    def on_stopped(self):
        print("I'm stopped")

    def on_receive(self, message):
        # Receive results from actor
        if message['distance'] < self.best_solution:
            self.best_solution = message['distance']
            self.solution = message['taken_vertices']
            print(str(self.solution) + "->" + str(self.best_solution))

        if self.best_solution is not 100000000:
            self.received += 1

        if self.tasks:
            work = self.tasks[0]
            self.tasks = self.tasks[1:]
            msg = {
                'taken_vertices' : work,
                'best_solution' : self.best_solution,
            }
            message['actor'].tell(msg)
        else:
            message['actor'].stop()

        if self.received == self.sent:
            print("DONE!")
            self.actor_ref.stop(block=False)
'''
routes = {0: {1 : 10, 2 : 15, 3 : 20, 4 : 50, 5 : 100, 6 : 35, 7 : 20},
          1: {0 : 10, 2 : 35, 3 : 25, 4 : 10, 5 : 45, 6 : 85, 7 : 50},
          2: {0 : 15, 1 : 35, 3 : 30, 4 : 70, 5 : 60, 6 : 60, 7 : 10},
          3: {0 : 20, 1 : 25, 2 : 30, 4 : 20, 5 : 45, 6 : 50, 7 : 60},
          4: {0 : 50, 1 : 10, 2 : 70, 3 : 20, 5 : 20, 6 : 25, 7 : 30},
          5: {0 : 100, 1 : 45, 2 : 60, 3 : 45, 4 :20, 6 : 55, 7 : 10},
          6: {0 : 35, 1 : 85, 2 : 60, 3 : 50, 4 : 25, 5 : 55, 7 : 65},
          7: {0 : 20, 1 : 50, 2 : 10, 3 : 60, 4 : 30, 5 : 10, 6 : 65}}

taken_edges = {0: {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0},
               1: {0 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0},
               2: {1 : 0, 0 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0},
               3: {1 : 0, 2 : 0, 0 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0},
               4: {1 : 0, 2 : 0, 3 : 0, 0 : 0, 5 : 0, 6 : 0, 7 : 0},
               5: {1 : 0, 2 : 0, 3 : 0, 4 : 0, 0 : 0, 6 : 0, 7 : 0},
               6: {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 0 : 0, 7 : 0},
               7: {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 0 : 0}}
'''

routes = {}
taken_edges = {}

for i in range(13):
    routes[i] = {}
    taken_edges[i] = {}
    for j in range(13):
        routes[i][j] = random.randint(1, 100)
        taken_edges[i][j] = 0
        

#Take two shortest edges for every vertex
for v1, edges in routes.items():
    for v2, _ in sorted(filter(lambda x: taken_edges[v1][x[0]] == 0, edges.items()), key=lambda x: x[1])[0:2]:
        taken_edges[v1][v2] = 1

executor = TSPExecutor
executor.use_daemon_thread = False
executor = executor.start(routes, 2, taken_edges, 0)

for _ in range(5):
    resolver = TSPResolver
    resolver.use_daemon_thread = False
    resolver.start(executor, routes, taken_edges)

executor.actor_stopped.wait()
