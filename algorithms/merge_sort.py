
# Сортировка слиянием
# Слияние отсортированных массивов в один
# Проходов: O * (N * log2(N))
# Выделение памяти: N * log2(N)

def merge(A: list, B: list):
    C = [0] * (len(A) + len(B))
    i = k = n = 0
    while i < len(A) and k < len(B):
        if A[i] <= B[k]:
            C[n] = A[i]
            i += 1
            n += 1
        else:
            C[n] = B[k]
            k += 1
            n += 1
    while i < len(A):
        C[n] = A[i]
        i += 1
        n += 1
    while k < len(B):
        C[n] = B[k]
        k += 1
        n += 1
    return C


def merge_sort(A: list):
    if len(A) <= 1:
        return
    middle = len(A) // 2
    L = [A[i] for i in range(middle)]
    R = [A[i] for i in range(middle, len(A))]
    merge_sort(L)
    merge_sort(R)
    C = merge(L, R)
    for i in range(len(A)):
        A[i] = C[i]

B = [5, 2, 7, 3, 1]
merge_sort(B)
print(*B)