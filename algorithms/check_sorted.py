
def check_sorted(A, ascending=True):
    """ Проверка отсортированности за O(len(A)) """
    flag = True
    s = 2 * int(ascending) - 1
    for i in range(len(A) - 1):
        if s * A[i] > s * A[i + 1]:
            flag = False
            break
    return flag
    