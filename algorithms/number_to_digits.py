x = 12345

L = list(map(int, str(x)))

L2 = [i for i in map(int, str(x))]

L3 = [int(i) for i in str(x)]

L4 = []
s = str(x)
for i in range(len(s)):
    L4.append(int(s[i]))

L5 = []
for i in str(x):
    L5.append(int(i))

L6 = []
new_x = x
while new_x > 0:
    L6.append(new_x % 10)
    new_x //= 10
L6.reverse()
