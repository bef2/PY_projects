
def fib(n):
    """ Вычисляет число Фибоначи, асимптотика O(n) """
    rec_fib =[0, 1] + [0] * (n -1)
    for i in range(2, n + 1):
        rec_fib[i] = rec_fib[i - 1] + rec_fib[i - 2]
    return rec_fib[n]

for i in range(20):
    print(fib(i), end='  ')