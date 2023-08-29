def count_sort(A):
    '''Сортировка подсчетом требует О(3N) по времени и О(N + len(spec)) по памяти'''
    spec = [0] * (max(A) + 1)
    for dig in A:
       spec[dig] += 1
    return [i for i in range(len(spec)) for j in range(spec[i])]



if __name__ == "__main__":
    L = [5, 3, 1, 6, 4, 2]
    print(count_sort(L))