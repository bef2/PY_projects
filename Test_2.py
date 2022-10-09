import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QWidget

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import random

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # экземпляр фигуры для построения
        self.figure = plt.figure()
        plt.title("Зависимости: y1 = x, y2 = x^2")
        plt.xlabel("x")
        plt.ylabel("y1, y2")
        plt.grid()

        # это виджет холста(Canvas), который отображает 'figure'
        # он принимает экземпляр `figure` в качестве параметра для __init__
        self.canvas = FigureCanvas(self.figure)

        # это виджет навигации
        # он принимает виджет холста(Canvas) и родителя
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Просто какая-то кнопка, связанная с методом `plot`
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        plt.yscale('log')

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())