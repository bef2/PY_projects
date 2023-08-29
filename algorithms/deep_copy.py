def deep_copy(A):
    return [elem if not isinstance(elem, list) 
            else deep_copy(elem) for elem in A]
    


if __name__ == "__main__":
    L = [[1], 2, [3, 4], 5]
    L2 = deep_copy(L)
    L[1] = 777
    L[2][0] = 888
    print(L)
    print(L2)