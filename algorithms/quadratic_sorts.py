# Квадратичные сортировки требуют по времеми О(N^2)
# Проходов: k * (N * (N - 1) / 2)


def insert_sort(A): # Рабтает быстрее в зависимости от состояния массива
    """ сортировка списка А вставками """
    for i in range(1, len(A)):
        tmp = i
        while tmp > 0 and A[tmp-1] > A[tmp]:
            A[tmp], A[tmp-1] = A[tmp-1], A[tmp]
            tmp -= 1
            
            
def insert_sort_fast(A):
    """Сортировка списка вставками"""
    for i in range(1, len(A)):
        tmp = A[i]
        j = i - 1
        while j >= 0 and A[j] > tmp:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = tmp

 
def choise_sort(A):
    """ сортировка списка А выбором """
    N = len(A)
    for pos in range(0, N - 1):
        for j in range(pos + 1, N):
            if A[j] < A[pos]:
                A[j], A[pos] = A[pos], A[j]


def bubble_sort(A):
    """ сортировка списка А методом пузырька """
    N = len(A)
    for bypass in range(1, N):
        for j in range(N - bypass):
            if A[j] > A[j+1]:
                A[j], A[j+1] = A[j+1], A[j]


def test_sort(sort_algorithm):
    print('Тестируем:', sort_algorithm.__doc__)

    print("testcase #1:", end='')
    A = [4, 2, 5, 1, 3]
    A_sorted = [1, 2, 3, 4, 5]
    sort_algorithm(A)
    print('Ok' if A == A_sorted else 'Fail')

    print("testcase #2:", end='')
    A = list(range(10, 20)) + list(range(10))
    A_sorted = list(range(20))
    sort_algorithm(A)
    print('Ok' if A == A_sorted else 'Fail')

    print("testcase #3:", end='')
    A = [4, 2, 4, 1, 2]
    A_sorted = [1, 2, 2, 4, 4]
    sort_algorithm(A)
    print('Ok' if A == A_sorted else 'Fail')


if __name__ == '__main__':
    test_sort(insert_sort)
    test_sort(choise_sort)
    test_sort(bubble_sort)
