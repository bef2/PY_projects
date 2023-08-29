# Рекурсивный обход в глубину
def sumtree(L):
    tot = 0
    for x in L:
        if not isinstance(x, list):
            tot += x
        else:
            tot += sumtree(x)
    return tot


# Без рекурсии обход в ширину
def sumtree2(L):
    tot = 0
    items = list(L)
    while items:
        front = items.pop(0)
        if not isinstance(front, list):
            tot += front
        else:
            items.extend(front)
    return tot


# Без рекурсии обход в глубину
def sumtree3(L):
    tot = 0
    items = list(L)
    while items:
        front = items.pop(0)
        if not isinstance(front, list):
            tot += front
        else:
            items[:0] = front
    return tot


if __name__ == '__main__':
    L = [1, [2, [3, 4], 5], 6, [7, 8]]
    print(sumtree(L))
    print(sumtree2(L))
    print(sumtree3(L))