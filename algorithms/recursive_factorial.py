
def factorial(n: int):
    assert n >= 0, "Факториал отрицательного неопределён."
    if n == 0:
        return 1
    return factorial(n - 1) * n

print(factorial(5))
