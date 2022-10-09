
# Сортировка Энтони Хоара
# Проходов: O * (N * log2(N))
# Выделение памяти: N * log2(N)


def hoare_sort(A: list):
    if len(A) <= 1:
        return
    barrier = A[len(A) // 2]
    L = []
    M = []
    R = []
    for x in A:
        if x < barrier:
            L.append(x)
        elif x == barrier:
            M.append(x)
        else:
            R.append(x)
    hoare_sort(L)
    hoare_sort(R)
    A[:] = L + M + R
   
B = [5, 2, 7, 3, 1]
hoare_sort(B)
print(*B)