def prime(n):
    '''Проверяет число на простоту. O(sqrt(n) / 2)'''
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n and n % d != 0:
        d += 2
    return d * d > n


def prime_num(n):
    '''Выводит N-е простое число'''
    if n < 1:
        raise ValueError('Requires a number greater than zero')
    d = 1
    while n > 0:
        d += 1
        if prime(d):
            n -= 1
    return d


def prime_list(n):
    '''Выводит N-е количество простых чисел'''
    if n < 0:
        raise ValueError("Can't use negative numbers")
    lst = []
    d = 1
    while n > 0:
        d += 1
        if prime(d):
            lst.append(d)
            n -= 1
    return lst

    
def prime_search(n):
    '''Находит все простые числа до N-го числа'''
    return [d for d in range(n) if prime(d)]


def erastophen(N):
    '''Находит все простые числа до N-го числа'''
    primes = [i for i in range(N + 1)]
    primes[1] = 0

    for i in range(N + 1):
        if primes[i] != 0:
            j = i + i
            while j <= N:
                primes[j] = 0
                j += i
       
    primes = [i for i in primes if i != 0]
    return primes


if __name__ == "__main__":
    from time import time
    
    x = 100_000
    
    s = time()
    erastophen(x)
    e = time()
    print(e - s)