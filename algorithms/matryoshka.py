def matryoshka(n):
    if n == 1:
        print('Матрёшечка')
    else:
        print('Вверх матрёшки n=', n)
        matryoshka(n - 1)
        print('Низ матрёшки n=', n)

matryoshka(5)