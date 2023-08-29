def gcd(a, b):
    '''Находит наибольший общий делитель'''
    if a == b:
        return a
    elif a > b:
        return gcd(a - b, b)
    else:   # a < b
        return gcd(a, b - a)


def gcd2(a ,b):
    '''Находит наибольший общий делитель'''
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def gcd3(a, b):
    '''Находит наибольший общий делитель'''
    return a if b == 0 else gcd(b, a % b)



if __name__ == "__main__":
    x = 3
    y = 7
    print(gcd(x, y))
    print(gcd2(x, y))
    print(gcd3(x, y))