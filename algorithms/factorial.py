def fact(n):
    '''Находит факториал числа n циклом while'''
    fac = 1
    while n > 1:
        fac *= n
        n -= 1
    return fac


def fact2(n):
    '''Находит факториал числа n циклом for'''
    fac = 1
    for i in range(2, n + 1):
        fac *= i
    return fac


def fact3(n):
    '''Находит факториал числа n рекурсией'''
    if n == 1:
        return 1
    return fact3(n - 1) * n



if __name__ == "__main__":
    x = 3
    print(fact(x))
    print(fact2(x))
    print(fact3(x))