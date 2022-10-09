
# Сортировка подсчетом требует О(N) по времени и О(М) по памяти

F = [0] * 10
for k in range(len(F)):
    x = int(input())
    F[x] += 1

for k in range(len(F)):
    print(str(k) * F[k], end='')