def factor(n: int) -> list:
    '''Находит простые множетили. Сложность O(sqrt(n))'''
    lst = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            lst.append(d)
        while n % d == 0:
            n //= d
        d += 1
    if n > 1:
        lst.append(n)
    return lst


def factor_all(n: int) -> list:
    '''Находит все множители. Сложность O(n / 2)'''
    lst = []
    d = 2
    while d <= n / 2:
        if n % d == 0:
            lst.append(d)
        d += 1
    return lst



if __name__ == "__main__":
    x = 777
    print(factor(x))
    print(factor_all(x))
