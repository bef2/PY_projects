
def count_trajectories(N: int, step: list, ban: list = []):
    """ Вычмсляет возможно количество траекторий из 1 в N
        с шагами step, ban - список запрещенных клеток
        значения, значения ban не должны быть больше N
    """
    allowed = [True] * (N + 1)
    for i in ban:
        allowed[i] = False
    K = [0, 1] + [1] * (len(step) - 1) + [0] * (N - len(step))
    for i in range(2, N + 1):
        if allowed[i]:
            sum = 0
            for k in step:
                sum += K[i - k]
            K[i] = sum
    return K[N]


if __name__ == "__main__":
    print(count_trajectories(6, [1, 2, 3], [4]))