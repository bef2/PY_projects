def gen_bin(M, prefix=""):
    """ Генерирует все числа (с лидирующими не значащами нулями)
        в 2-ичной системе счисления длины М
    """
    if M == 0:
        print(prefix)
        return
    gen_bin(M-1, prefix+"0")
    gen_bin(M-1, prefix+"1")


def generate_number(N: int, M: int, prefix=None):
    """ Генерирует все числа (с лидирующими не значащами нулями)
        в N-ричной системе счисления (N <= 10) длины М
    """
    prefix = prefix or []
    if M == 0:
        print(*prefix)
        return
    for dig in range(N):
        prefix.append(dig)
        generate_number(N, M-1, prefix)
        prefix.pop()


def generate_permutations(N: int, M: int =-1, prefix=None):
    """ Генерация всех перестановок N чисел в M позициях
        с префиксом prefix.
    """
    if N > M and type(N) != int and type(M) != int:
        raise ValueError("Bad function parameters")  
      
    M = N if M == -1 else M
    prefix = prefix or []
    
    if M == 0:
        print(*prefix)
        return
    
    for num in range(1, N+1):
        if num in prefix: continue
        prefix.append(num)
        generate_permutations(N, M-1, prefix)
        prefix.pop()



if __name__ == "__main__":
    generate_number(10, 2)