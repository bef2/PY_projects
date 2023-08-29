def shift(lst, steps):
    if steps < 0:
        steps = abs(steps)
        for i in range(steps):
            lst.append(lst.pop(0))
    else:
        for i in range(steps):
            lst.insert(0, lst.pop())



if __name__ == "__main__":
    lst = [1, 2, 3, 4, 5]
    shift(lst, -2)
    print(lst)