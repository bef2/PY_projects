
def pow(a: float, n: int):
    """ Быстрое возведение в степень """
    assert a >= 0
    assert n >= 0 and type(n) == int
    if n == 0:
        return 1
    elif n % 2 == 1:    # n - нечётное
        return pow(a, n - 1) * a
    else:   # n - чётное
        return pow(a ** 2, n // 2)


print(pow(2, 5))