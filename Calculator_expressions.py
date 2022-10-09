from math import*


print('\n======================КАЛЬКУЛЯТОР =======================')
print('=== Для выхода введите "exit", для справки - "reference". ===\n')

reference = """    ceil(X) – округление до ближайшего большего числа.
    copysign(X, Y) - возвращает число, имеющее модуль такой же, как и у числа X, а знак - как у числа Y.
    fabs(X) - модуль X.
    factorial(X) - факториал числа X.
    floor(X) - округление вниз.
    fmod(X, Y) - остаток от деления X на Y.
    frexp(X) - возвращает мантиссу и экспоненту числа.
    ldexp(X, I) - X * 2^i. Функция, обратная функции math.frexp().
    fsum(последовательность) - сумма всех членов последовательности. Эквивалент встроенной функции sum(), но math.fsum() более точна для чисел с плавающей точкой.
    isfinite(X) - является ли X числом.
    isinf(X) - является ли X бесконечностью.
    isnan(X) - является ли X NaN (Not a Number - не число).
    modf(X) - возвращает дробную и целую часть числа X. Оба числа имеют тот же знак, что и X.
    trunc(X) - усекает значение X до целого.
    exp(X) - e^X.
    expm1(X) - e^X - 1. При X -> 0 точнее, чем math.exp(X)-1.
    log(X, [base]) - логарифм X по основанию base. Если base не указан, вычисляется натуральный логарифм.
    log1p(X) - натуральный логарифм (1 + X). При X -> 0 точнее, чем math.log(1+X).
    log10(X) - логарифм X по основанию 10.
    log2(X) - логарифм X по основанию 2.
    pow(X, Y) - X^Y.
    sqrt(X) - квадратный корень из X.
    acos(X) - арккосинус X. В радианах.
    asin(X) - арксинус X. В радианах.
    atan(X) - арктангенс X. В радианах.
    atan2(Y, X) - арктангенс Y/X. В радианах. С учетом четверти, в которой находится точка (X, Y).
    cos(X) - косинус X (X указывается в радианах).
    sin(X) - синус X (X указывается в радианах).
    tan(X) - тангенс X (X указывается в радианах).
    hypot(X, Y) - вычисляет гипотенузу треугольника с катетами X и Y (math.sqrt(x * x + y * y)).
    degrees(X) - конвертирует радианы в градусы.
    radians(X) - конвертирует градусы в радианы.
    cosh(X) - вычисляет гиперболический косинус.
    sinh(X) - вычисляет гиперболический синус.
    tanh(X) - вычисляет гиперболический тангенс.
    acosh(X) - вычисляет обратный гиперболический косинус.
    asinh(X) - вычисляет обратный гиперболический синус.
    atanh(X) - вычисляет обратный гиперболический тангенс.
    erf(X) - функция ошибок.
    erfc(X) - дополнительная функция ошибок (1 - math.erf(X)).
    gamma(X) - гамма-функция X.
    lgamma(X) - натуральный логарифм гамма-функции X.
    pi = 3,1415926...
    e  = 2,718281..."""
print('Введите выражение:')
while True:
    try:
        expression = input('> ')
        if '[' in expression or '{' in expression\
            or "'" in expression or ',' in expression:
            raise ValueError
        if expression == 'exit':
            break
        if expression == 'reference':
            print(reference)
            continue
        calculate = eval(compile(expression, '<string>', 'eval'))
        print('=', calculate, '\n')
    except Exception:
        print('Неверный ввод')