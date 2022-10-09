import matplotlib.pyplot as plt
import numpy as np


# Линейная зависимость
x = np.linspace(0, 10, 50)
y1 = x

# Квадратичная зависимость
y2 = [i**2 for i in x]

plt.title("Зависимости: y1 = x, y2 = x^2")
plt.xlabel("x")
plt.ylabel("y1, y2")
plt.grid()
plt.plot(x, y1, x, y2)

plt.show()