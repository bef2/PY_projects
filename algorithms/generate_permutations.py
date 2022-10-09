
def find(number, A):
    """ Ищет x в A и возвращает True, если такой есть,
        False - если нет
    """
    for k in A:
        if number == k:
            return True
    return False


def generate_permutations(N: int, M: int = -1, prefix=None):
    """ Генерация всех перестановок N чисел в M позициях
        с префиксом prefix.
    """
    assert M <= N and type(N) == int and type(M) == int
    M = N if M == -1 else M  # по умолчанию N чисел в N позициях
    prefix = prefix or []
    if M == 0:
        print(*prefix) 
        return 
    for number in range(1, N + 1):
        if find(number, prefix):
            continue
        prefix.append(number)
        generate_permutations(N, M - 1, prefix)
        prefix.pop()

generate_permutations(3)