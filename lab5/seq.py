import copy
import time

best_solution = 1000000
solution = []

def calculate_distance(routes, taken_edges):
    distance = 0
    for v1, edges in taken_edges.items():
        distance += sum([routes[v1][a[0]] for a in filter(lambda x: taken_edges[v1][x[0]] != 0, edges.items())])
    return distance/2

def compute(routes, taken_edges, distance, taken_vertices):
    global best_solution
    global solution

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
        

routes = {0: {0: 45, 1: 54, 2: 8, 3: 3, 4: 68, 5: 69, 6: 89, 7: 8, 8: 60, 9: 13, 10: 11, 11: 65, 12: 84}, 1: {0: 74, 1: 47, 2: 3, 3: 2, 4: 14, 5: 39, 6: 16, 7: 6, 8: 30, 9: 7, 10: 36, 11: 44, 12: 69}, 2: {0: 49, 1: 98, 2: 99, 3: 32, 4: 3, 5: 47, 6: 56, 7: 91, 8: 61, 9: 24, 10: 12, 11: 33, 12: 28}, 3: {0: 46, 1: 16, 2: 32, 3: 30, 4: 32, 5: 36, 6: 12, 7: 98, 8: 85, 9: 22, 10: 35, 11: 5, 12: 52}, 4: {0: 21, 1: 73, 2: 59, 3: 96, 4: 94, 5: 42, 6: 86, 7: 22, 8: 82, 9: 62, 10: 55, 11: 100, 12: 71}, 5: {0: 42, 1: 88, 2: 28, 3: 52, 4: 1, 5: 44, 6: 43, 7: 100, 8: 28, 9: 59, 10: 78, 11: 7, 12: 39}, 6: {0: 52, 1: 10, 2: 39, 3: 95, 4: 96, 5: 84, 6: 49, 7: 5, 8: 35, 9: 24, 10: 56, 11: 24, 12: 75}, 7: {0: 87, 1: 48, 2: 27, 3: 51, 4: 83, 5: 22, 6: 81, 7: 23, 8: 57, 9: 12, 10: 29, 11: 65, 12: 28}, 8: {0: 38, 1: 41, 2: 33, 3: 69, 4: 87, 5: 83, 6: 87, 7: 25, 8: 99, 9: 76, 10: 25, 11: 78, 12: 78}, 9: {0: 22, 1: 84, 2: 99, 3: 85, 4: 76, 5: 3, 6: 44, 7: 68, 8: 52, 9: 68, 10: 46, 11: 58, 12: 72}, 10: {0: 32, 1: 66, 2: 14, 3: 17, 4: 59, 5: 36, 6: 37, 7: 49, 8: 70, 9: 19, 10: 2, 11: 67, 12: 14}, 11: {0: 88, 1: 6, 2: 77, 3: 15, 4: 63, 5: 64, 6: 44, 7: 12, 8: 59, 9: 1, 10: 89, 11: 19, 12: 72}, 12: {0: 72, 1: 39, 2: 34, 3: 80, 4: 8, 5: 100, 6: 64, 7: 10, 8: 53, 9: 33, 10: 85, 11: 90, 12: 39}}
taken_edges = {0: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}, 1: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}, 2: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}, 3: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}, 4: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}, 5: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}, 6: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}, 7: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}, 8: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}, 9: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}, 10: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}, 11: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}, 12: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}}

total_time = -time.perf_counter()

#Take two shortest edges for every vertex
for v1, edges in routes.items():
    for v2, _ in sorted(filter(lambda x: taken_edges[v1][x[0]] == 0, edges.items()), key=lambda x: x[1])[0:2]:
        taken_edges[v1][v2] = 1

lower_bound = calculate_distance(routes, taken_edges)
print("Lower bound: " + str(lower_bound))

root_node = 0
compute(routes, copy.deepcopy(taken_edges), lower_bound, [root_node])

print("Result:")
print(solution)
print(best_solution)

total_time += time.perf_counter()
print("1, " + str(total_time))
