import numpy as np


# срез исключений из матрицы
# ~np.in1d(np.arange(МАТРИЦА.shape[1]), [СТОЛБЦЫ_ДЛЯ_ИСКЛЮЧЕНИЯ])


def dual_simplex(A, b, c, B):
    def iteration(y, B):
        nonlocal A
        nonlocal c
        nonlocal b

        # 1. обратная матрица
        Abase = A[:, B]
        Abase_inv = np.linalg.inv(Abase)

        # 2. каппы
        aes = np.zeros(len(A[0]))
        aesbase = np.dot(Abase_inv, b)
        for i in range(len(aesbase)):
            aes[B[i]] = aesbase[i]

        # 3. Проверка на конец
        if np.min(aes) >= 0:
            print(f"{aes} - admissible plan for direct problem\n{y} - ... for dual problem")
            return aes, y
        # 4. j0*
        iae = np.where(aes < 0)[0][0]
        j0star = np.where(B == iae)[0][0]

        # 5. delta_y
        y_delta = Abase_inv[j0star]

        # 6. mu, N
        N = np.array(range(len(A[0])))
        N = N[~np.isin(np.arange(N.size), B)]

        mus = {}
        for j in N:
            Aj = A[:, j]
            mus[j] = np.dot(y_delta, Aj)

        # 7. Проверка на совместность
        if min(mus.values()) >= 0:
            print('the problem is incompatible')
            return None

        # 8. sigmas
        sigmas = {}
        for j in N:
            if mus[j] >= 0:
                continue
            sigmas[j] = (c[j] - np.dot(A[:, j], y))/mus[j]

        # 9. j0
        sigmamin = min(sigmas.values())
        j0 = 0
        for key in sigmas.keys():
            if sigmas[key] == sigmamin:
                j0 = key
                break

        # коррекция y и B
        B[j0star] = j0
        y = y + sigmamin*y_delta
        return iteration(y, B)

    A_base = A[:, B]
    cbase = c[B]
    y = np.dot(cbase, np.linalg.inv(A_base))

    return iteration(y, B)


A = np.array([[-2, -1, -4, 1, 0],
              [-2, -2, -2, 0, 1]])
B = np.array([3, 4])
b = (-1, -3/2)
c = np.array([-4,-3,-7,0,0])

dual_simplex(A, b, c, B)