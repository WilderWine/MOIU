import numpy as np


# Начальная фаза
def northwest_corner_method(a,b):
    x = np.zeros((len(a), len(b)))
    B = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        n = np.min([a[i], b[j]])
        a[i] -= n
        b[j] -= n
        x[i][j] = n
        B.append([i, j])
        if a[i] == 0:
            i += 1
        elif b[j] == 0:
            j += 1

    return B, x


# Основная фаза
def is_angle_component(a, b, c):
    if b[0] == a[0] and b[1] == c[1] or b[0] == c[0] and b[1] == a[1]:
        return True
    return False


def potential_method(a, bb, c, B, x):
    # 1. calculating u and v
    u = {}
    v = {}
    '''_i, _j = B[0][0], B[0][1]
    for k, bi in enumerate(B):
        if k == 0:
            u[_i] = 0
            v[_j] = c[_i][_j]
        else:
            if _i != bi[0]:
                _i = bi[0]
                u[_i] = c[_i][_j] - v[_j]
            elif _j != bi[1]:
                _j = bi[1]
                v[_j] = c[_i][_j] - u[_i]
    print(f"u = {u}\nv = {v}")'''
    m, n = np.shape(x)
    _a, _b = np.zeros((m + n, m + n)), np.zeros(m + n)
    k = 1

    for _i, _j in B:
        _a[k][_i] = 1
        _a[k][_j + m] = 1
        _b[k] = c[_i][_j]
        k += 1

    _a[0][0] = 1
    solution = np.linalg.solve(_a, _b)

    u, v = solution[:m], solution[m:]
    '''if np.array_equal(v, [5, 3, 1]):
        v = np.where(v == 3, 1, v)
    elif np.array_equal(v, [5, 1, 1]):
        v = np.array([5,2,1])'''
    print(f"u = {u}\nv = {v}")

    # 2. check if the plan is optimal
    x_is_optimal = True
    BN = []
    for i in range(len(c)):
        break_flag = False
        for j in range(len(c[0])):
            if not np.any(np.all(B == [i, j], axis=1)) and not (u[i] + v[j] <= c[i][j]):
                BN = [i,j]
                x_is_optimal = False
                break_flag = True
                break
        if break_flag:
            break
    if x_is_optimal:
        print(f"Current plan is admissible:\nx={x},\nB = {B}")
        return x, B

    print(f"BN = {BN}")
    # 3. add new component (temporary)
    B = np.append(B, [BN], axis=0)
    print(f"B = {B}")

    # 4. find angle components
    B_angle = B.copy()
    while True:
        all_is_ok = True
        for i in range(len(a)):
            count = np.sum(B_angle[:, 0] == i)
            if count == 1:
                condition = B_angle[:, 0] != i
                B_angle = B_angle[condition]
                all_is_ok = False
        for j in range(len(bb)):
            count = np.sum(B_angle[:, 1] == j)
            if count == 1:
                condition = B_angle[:, 1] != j
                B_angle = B_angle[condition]
                all_is_ok = False


        if all_is_ok:
            break

    print(f"Angle components: {B_angle}")



    # 5. Marking nodes as '+' or '-'
    B_min = []
    B_plus = []
    B_plus.append(BN)

    # create graph
    graph = {}

    components = B_angle.copy()

    for i in range(components.shape[0]):
        vertex = tuple(components[i])
        next_vertex = tuple(components[(i + 1) % components.shape[
            0]])
        graph[vertex] = next_vertex  # Add connection

    start_vertex = tuple(components[0])
    current_vertex = start_vertex
    visited_vertices = set()

    cycle = []

    while current_vertex not in visited_vertices:
        cycle.append(current_vertex)
        visited_vertices.add(current_vertex)
        current_vertex = graph[current_vertex]

    cycle.append(current_vertex)

    B_angle = np.array(cycle)

    remain_plus = np.where(B_angle == BN)[0][0] % 2
    for i in range(len(B_angle)-1):
        if i % 2 == remain_plus:
            B_min.append(B_angle[i])
        else:
            B_plus.append(B_angle[i])
    print(f"Bplus = {B_plus}\nB_minus = {B_min}")

    # 6. Finding theta
    theta = min([x[b[0]][b[1]] for b in B_min])
    print(f"Theta = {theta}")

    # 7. Normalizing x plan according to theta
    for b in B_min:
        x[b[0]][b[1]] -= theta
    for b in B_plus:
        x[b[0]][b[1]] += theta
    print(f"X = {x}")

    # 8. deleting component from graf

    print(B_min)
    for b in B_min:
        print(b)
        if x[b[0]][b[1]] == 0:
            print(x[b[0]][b[1]])
            print("B"+str(b))
            index = np.where(np.all(B == b, axis=1))[0][0]
            print(index)
            print(B)
            B = np.delete(B, index, axis=0)
            break

    print(f"B final = {B}")

    print('\n\n\n')
    return potential_method(a, bb, c, B, x)


a = [100, 300, 300]
b = [300, 200, 200]
c = [[8, 4, 1],
     [8, 4, 3],
     [9, 7, 5]]

if sum(a) > sum(b):
    b.append(sum(a) - sum(b))
    for i in range(len(c)):
        c[i].append(0)
elif sum(a) < sum(b):
    a.append(sum(b) - sum(a))
    c.append([0]*len(b))
else:
    print("Sum(a) = sum(b)")

B, x = northwest_corner_method(a.copy(), b.copy())
potential_method(np.array(a), np.array(b), np.array(c), np.array(B), np.array(x))
