
def generate_numbers(N: int, M: int, prefix=None):
    """ Генерирует все числа (с лидирующими нулями)
        в N-ричнчной системе счисления (2 <= N <= 10) длины M
    """
    # M = N if M == -1 else M  # по умолчанию N чисел в N позициях
    assert type(N) == int and 2 <= N <= 10
    assert type(M) == int
    prefix = prefix or []
    if M == 0:
        print(*prefix)
        return
    for digit in range(N):
        prefix.append(digit)
        generate_numbers(N, M - 1, prefix)
        prefix.pop()

generate_numbers(3, 3)