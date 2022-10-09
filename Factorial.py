from time import perf_counter


def factorial(digit):
    """ Вычисляет факториал аргумента digit.
        digit >= 0, digit - целое число.
    """
    if digit < 0:
        raise ValueError('Факториал отрицательного не определён')
    if type(digit) != int:
        raise ValueError('Факториал нецелого числа не определён')
    if digit == 0:
        return 1  
    
    result = 1
    for iter in range(1, digit + 1):
        result *= iter
    return result


if __name__ == "__main__":
    while True:
        user_input = input('Введите число для вычисления факториала:')
        if user_input == 'exit':
            break
        elif user_input.isdigit():
            print(factorial(int(user_input)))
        else:
            print('Неверный ввод, повторите.')