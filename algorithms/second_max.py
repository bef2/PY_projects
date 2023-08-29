# Нахождение второго максимума за один проход

L = [3, 6, 1, 2, 8, 5]

max1 = L[0]
max2 = L[1]
if max1 < max2:
        max1, max2 = max2, max1
for i in range(2, len(L)):
    if L[i] > max2:
        max2 = L[i]
    if max1 < max2:
        max1, max2 = max2, max1