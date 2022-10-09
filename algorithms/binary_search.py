
# Бинарный поиск в массиве. Скорость O(log2(N))
# Главное условие - массив отсортирован по возрастанию


def check_sorted(A, ascending=True):
    """ Проверка отсортированности за O(len(A)) """
    flag = True
    s = 2 * int(ascending) - 1
    for i in range(len(A) - 1):
        if s * A[i] > s * A[i + 1]:
            flag = False
            break
    return flag


def left_bound(A, key):
    left = -1
    right = len(A)
    while right - left > 1:
        middle = (left + right) // 2
        if A[middle] < key:
            left = middle
        else:
            right = middle
    return left


def right_bound(A, key):
    left = -1
    right = len(A)
    while right - left > 1:
        middle = (left + right) // 2
        if A[middle] <= key:
            left = middle
        else:
            right = middle
    return right


def bin_search(A, key):
    if not check_sorted(A):
        raise ValueError('Попытка поиска по несортированному массиву.')
    left = left_bound(A, key)
    right = right_bound(A, key)
    if right - left > 1:
        return left + 1
    return
