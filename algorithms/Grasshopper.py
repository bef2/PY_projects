# Сколько различных траекторий допрыгать из 1 в N
# с шагами 1, 2, 3, ban - список запрещенных клеток
# значения ban не должны быть больше N


def grasshopper(N: int, ban: list = []):
    allowed = [True] * (N + 1)
    for i in ban:
        allowed[i] = False
    K = [0, 1, int(allowed[2])] + [0] * (N - 2)
    for i in range(3, N + 1):
        if allowed[i]:
            K[i] = K[i - 1] + K[i - 2] + K[i - 3]
    return K[N]


print(grasshopper(5))
