def __fact(N):
    '''Возвращает факториал от N.'''
    if N < 0 or type(N) != int:
        raise ValueError("Required int >= 0")
    mul = 1
    for i in range(2, N+1):
        mul *= i
    return mul


def permutation(N: int, M: int =-1) -> int:
    ''' Возвращает количество перестановок
        из N элементов по M позициям без повторений.
    '''
    if type(N) != int or type(M) != int:
        raise ValueError("Required int")
    if N <= 0 or M <= 0: return 0
    if M > N:
        raise ValueError("must N > M")
    
    M = N if M == -1 else M
    return int(__fact(N) / __fact(N - M))


def product(N: int, M: int =-1) -> int:
    ''' Возвращает количество размещений
        из N элементов по M позициям с повторениями.
    '''
    M = N if M == -1 else M
    if type(N) != int or type(M) != int or N < 0 or M < 1:
        raise ValueError("Required int >= 0")
    return N ** M


def combination(N: int, M: int) -> int:
    ''' Возвращает количество сочетаний
        из N элементов по M позициям без повторений.
    '''
    if type(N) != int or type(M) != int:
        raise ValueError("Required int")
    if M > N:
        raise ValueError("must N > M")
    if N <= 0 or M <= 0: return 0
    
    return int(__fact(N) / __fact(N-M) / __fact(M))


def combination_replace(N: int, M: int) -> int:
    ''' Возвращает количество сочетаний
        из N элементов по M позициям с повторениями.
    '''
    if type(N) != int or type(M) != int:
        raise ValueError("Required int")
    if M > N:
        raise ValueError("must N > M")
    if N <= 0 or M <= 0: return 0
    
    return int(__fact(N+M-1) / __fact(M) / __fact(N-1))
