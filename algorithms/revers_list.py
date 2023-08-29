def revers_list(lst):
    for i in range(len(lst) // 2):
        lst[i], lst[-1 - i] = lst[-1 - i], lst[i]
    return lst


if __name__ == "__main__":
    lst = [3, 5, 1, 4, 2]
    print(revers_list(lst))