
# Находит наибоьший общий делитель
def gcd(a, b):
    if a == b:
        return a
    elif a > b:
        return gcd(a - b, b)
    else:   # a < b
        return gcd(a, b - a)

def gcd2(a ,b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def gcd3(a, b):
    return a if b == 0 else gcd(b, a % b)

print(gcd3(6, 9))